from sqlalchemy import Table, create_engine, select, insert, exists
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import json
import sys
import os
from pprint import pprint

def get_connection():
    engine = create_engine('postgresql://acsherrock@localhost:5432/acsherrock')
    return engine.connect()

def get_tweet_files(directory=""):
    tweet_files = []
    for dirn, subdirs, filelist in os.walk(directory):
        for file in filelist:
            tweet_files.append(file)
    return tweet_files

def load_tweets(session):
    for filename in get_tweet_files(directory="tweets/"):
        file = "tweets/" + filename
        with open(file, 'r') as json_file:
            try:
                data = json.load(json_file)
                if type(data) == type([]):
                    for t in data:
                        if 'limit' not in t.keys():
                            session_add_tweet(session, t)
                os.rename(file, 'tweets-finished/' + filename)
            except json.decoder.JSONDecodeError as e:
                print("Last File: ", file, "\n",  e)
            except AttributeError as e:
                print("\nLast File: ", file, "\n", e)
                sys.exit()
            except KeyboardInterrupt:
                print("\nLast File: ", file)
                sys.exit()



def is_key(str, dict):
    return str in dict.keys() and dict[str] is not None and not dict[str] == 'null'

def session_add_user(session, user_json):
    (row_already_exists, ), = session.query(exists().where(User.id == user_json['id']))
    if not row_already_exists:
        user = User(**user_json)
        session.add(user)
        session.flush()
    return user_json['id']

def session_add_coordinates(session, coordinates_json):
    coord_ids = []
    if len(coordinates_json) == 2:
        coord_obj = Coordinates(longitude=coordinates_json[0], latitude=coordinates_json[1])
        session.add(coord_obj)
        session.flush()
        coord_ids.append(coord_obj.id)
    else:
        for coord in coordinates_json:
            coord_obj = Coordinates(longitude=coord[0], latitude=coord[1])
            session.add(coord_obj)
            session.flush()
            coord_ids.append(coord_obj.id)
    return coord_ids

def session_add_place(session, place_json):
    (row_already_exists, ), = session.query(exists().where(Place.id == place_json['id']))
    if not row_already_exists \
            and is_key('bounding_box', place_json) \
            and is_key('coordinates', place_json['bounding_box']):
        place_json['attributes'] = str(place_json['attributes'])
        coordinate_ids = session_add_coordinates(session, place_json['bounding_box']['coordinates'][0])
        location = Location(type=place_json['bounding_box']['type'], coordinates=coordinate_ids)
        session.add(location)
        session.flush()
        place_json['bounding_box'] = location.id
        place = Place(**place_json)
        session.add(place)
        session.flush()
    return place_json['id']


def session_add_tweet(session, tweet_json):
    (row_already_exists, ), = session.query(exists().where(Tweet.id == tweet_json['id']))
    if not row_already_exists:
        if is_key('retweeted_status', tweet_json):
            retweeted_tid = session_add_tweet(session, tweet_json['retweeted_status'])
            tweet_json['retweeted_status'] = retweeted_tid

        if is_key('quoted_status', tweet_json):
            quoted_tid = session_add_tweet(session, tweet_json['quoted_status'])
            tweet_json['quoted_status'] = quoted_tid

        if is_key('coordinates', tweet_json):
            geo_id = session_add_coordinates(session, tweet_json['coordinates']['coordinates'])
            tweet_json['coordinates'] = geo_id

        if is_key('geo', tweet_json):
            geo_id = session_add_coordinates(session, tweet_json['geo']['coordinates'])
            tweet_json['geo'] = geo_id

        if is_key('place', tweet_json):
            geo_id = session_add_place(session, tweet_json['place'])
            tweet_json['place'] = geo_id

        if is_key('scopes', tweet_json):
            tweet_json['scopes'] = str(tweet_json['scopes'])

        uid = session_add_user(session, tweet_json['user'])
        tweet_json['entities'] = str(tweet_json['entities'])
        tweet_json['user'] = uid
        tweet = Tweet(**tweet_json)
        session.add(tweet)
        session.flush()
        session.commit()
    return tweet_json['id']



Base = automap_base()
engine = create_engine('postgresql://acsherrock@localhost:5432/acsherrock')
Base.prepare(engine, reflect=True)

User = Base.classes.users
Tweet = Base.classes.tweets
Location = Base.classes.location
Coordinates = Base.classes.coordinates
Place = Base.classes.places
session = Session(engine)
load_tweets(session)

