from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, BOOLEAN, ENUM, FLOAT, INTEGER, JSON, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column


# ORM declarative base metaclass
orm_base = declarative_base()

class User(orm_base):
    """
    User table wrapper class.
    """

    __tablename__ = 'users'

    id = Column(BIGINT, primary_key=True)
    name = Column(TEXT)
    screen_name = Column(VARCHAR)
    description = Column(TEXT)
    favourites_count = Column(INTEGER)
    followers_count = Column(INTEGER)
    friends_count = Column(INTEGER)
    geo_enabled = Column(BOOLEAN)
    is_translator = Column(BOOLEAN)
    location = Column(JSON)
    lang = Column(TEXT)
    listed_count = Column(INTEGER)
    notifications = Column(BOOLEAN)
    protected = Column(BOOLEAN)
    show_all_inline_media = Column(BOOLEAN)
    status = Column(BIGINT)
    statuses_count = Column(INTEGER)
    time_zone = Column(TEXT)
    utc_offset = Column(INTEGER)
    verified = Column(BOOLEAN)
    withheld_in_countried = Column(TEXT)
    withheld_scope = Column(TEXT)
    profile_background_color = Column(TEXT)
    profile_background_image_url = Column(TEXT)
    profile_background_image_url_https = Column(TEXT)
    profile_background_tile = Column(BOOLEAN)
    profile_banner_url = Column(TEXT)
    profile_image_url = Column(TEXT)
    profile_image_url_https = Column(TEXT)
    profile_link_color = Column(TEXT)
    profile_sidebar_border_color = Column(TEXT)
    profile_sidebar_fill_color = Column(TEXT)
    profile_text_color = Column(TEXT)
    profile_use_background_image = Column(TEXT)
    entities = Column(ARRAY(BIGINT))
    default_profile = Column(BOOLEAN)
    default_profile_image = Column(BOOLEAN)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)
