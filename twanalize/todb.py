from sqlalchemy import Table, Column, create_engine, select, insert
from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, BOOLEAN, ENUM, FLOAT, INTEGER, JSON, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import operators
from sqlalchemy.orm import Session

import json
import os
from pprint import pprint


def get_connection():
    engine = create_engine('postgresql://acsherrock@localhost:5432/acsherrock')
    return engine.connect()

def get_tweet_files(directory=""):
    tweet_files = []
    for dirn, subdirs, filelist in os.walk(directory):
        for file in filelist:
            tweet_files.append(directory + file)
    return tweet_files


def load_tweets():
    for file in get_tweet_files(directory="../tweets/"):
        with open(file, 'r') as json_file:
            data = json.load(json_file)
            return data




Base = automap_base()
engine = create_engine('postgresql://acsherrock@localhost:5432/acsherrock')
Base.prepare(engine, reflect=True)


user_json = load_tweets()['user']


User = Base.classes.users
session = Session(engine)
session.add(User(**user_json))
# session.add(User(id=user_json['id'], name=user_json['name'], screen_name=user_json['screen_name'], description=user_json['description'], default_profile=user_json['default_profile'], default_profile_image=user_json['default_profile_image'], favorites_count=user_json['favourites_count'], followers_count=user_json['followers_count'], friends_count=user_json['friends_count'], geo_enabled=user_json['geo_enabled'], is_translator=user_json['is_translator'], lang=user_json['lang'], listed_count=user_json['listed_count'], notifications=user_json['notifications'], protected=user_json['protected'], show_all_inline_media=user_json['show_all_inline_media'], status=user_json['status'], statuses_count=user_json['statuses_count'], time_zone=user_json['time_zone'], utc_offset=user_json['utc_offset'], verified=user_json['verified'], withheld_in_countried=user_json['withheld_in_countried'], withheld_scope=user_json['withheld_scope'], profile_background_color=user_json['profile_background_color'], profile_background_image_url=user_json['profile_background_image_url'], profile_background_image_url_https=user_json['profile_background_image_url_https'], profile_background_tile=user_json['profile_background_tile'], profile_banner_url=user_json['profile_banner_url'], profile_image_url=user_json['profile_image_url'], profile_image_url_https=user_json['profile_image_url_https'], profile_link_color=user_json['profile_link_color'], profile_sidebar_border_color=user_json['profile_sidebar_border_color'], profile_sidebar_fill_color=user_json['profile_sidebar_fill_color'], profile_text_color=user_json['profile_text_color'], profile_use_background_image=user_json['profile_use_background_image'], entities=user_json['entities'], location=user_json['location']))



# # ORM declarative base class
# Base = declarative_base()
#
# class User(Base):
#     """
#     User table wrapper class.
#
#     """
#     __tablename__ = 'users'
#
#     id = Column(BIGINT, primary_key=True)
#     name = Column(TEXT)
#     screen_name = Column(VARCHAR)
#     description = Column(TEXT)
#     default_profile = Column(BOOLEAN)
#     default_profile_image = Column(BOOLEAN)
#     favorites_count = Column(INTEGER)
#     followers_count = Column(INTEGER)
#     friends_count = Column(INTEGER)
#     geo_enabled = Column(BOOLEAN)
#     is_translator = Column(BOOLEAN)
#     lang = Column(TEXT)
#     listed_count = Column(INTEGER)
#     notifications = Column(BOOLEAN)
#     protected = Column(BOOLEAN)
#     show_all_inline_media = Column(BOOLEAN)
#     status = Column(BIGINT)
#     statuses_count = Column(INTEGER)
#     time_zone = Column(TEXT)
#     utc_offset = Column(INTEGER)
#     verified = Column(BOOLEAN)
#     withheld_in_countried = Column(TEXT)
#     withheld_scope = Column(TEXT)
#     profile_background_color = Column(TEXT)
#     profile_background_image_url = Column(TEXT)
#     profile_background_image_url_https = Column(TEXT)
#     profile_background_tile = Column(BOOLEAN)
#     profile_banner_url = Column(TEXT)
#     profile_image_url = Column(TEXT)
#     profile_image_url_https = Column(TEXT)
#     profile_link_color = Column(TEXT)
#     profile_sidebar_border_color = Column(TEXT)
#     profile_sidebar_fill_color = Column(TEXT)
#     profile_text_color = Column(TEXT)
#     profile_use_background_image = Column(TEXT)
#     entities = Column(ARRAY(BIGINT))
#     location = Column(JSON)
#
#     def __repr__(self):
#         return "<User(id='%s', name='%s')>" % (self.id, self.name)