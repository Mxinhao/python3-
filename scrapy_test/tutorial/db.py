# -*-coding:utf-8-*-  
# !/usr/bin/python
import pymysql
from tutorial import config

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, or_, not_

Base = declarative_base()

class ToutiaoArticleList(Base):
    __tablename__ = 'c_toutiao_article_list'
    id = Column(BIGINT, primary_key=True)
    mp_name = Column(VARCHAR(30))
    source = Column(VARCHAR(100))
    image_url=Column(VARCHAR(200))
    single_mode = Column(TINYINT)
    abstract=Column(VARCHAR(1000))
    title = Column(VARCHAR(200))
    image_list = Column(TEXT)
    more_mode = Column(TINYINT)
    tag = Column(VARCHAR(100))
    tag_url = Column(VARCHAR(100))
    chinese_tag = Column(VARCHAR(100))
    group_source = Column(INTEGER)
    comments_count = Column(INTEGER)
    media_url = Column(VARCHAR(100))
    media_avatar_url = Column(VARCHAR(100))
    go_detail_count = Column(INTEGER)
    middle_mode = Column(TINYINT)
    gallary_image_count = Column(INTEGER)
    detail_play_effective_count = Column(INTEGER)
    video_duration_str = Column(VARCHAR(20))
    source_url = Column(VARCHAR(100))
    article_genre = Column(VARCHAR(20))
    display_url = Column(VARCHAR(500))
    behot_time =Column(DATETIME)
    has_gallery = Column(TINYINT)
    group_id=Column(BIGINT)
    create_time = Column(DATETIME)
    update_time = Column(DATETIME)

class ToutiaoArticleHistory(Base):
    __tablename__ = 'c_toutiao_article_history'
    id = Column(BIGINT, primary_key=True)
    sort=Column(INTEGER, primary_key=True)
    type=Column(VARCHAR(10), primary_key=True)
    mp_name = Column(VARCHAR(30))
    source = Column(VARCHAR(100))
    title = Column(VARCHAR(200))
    chinese_tag = Column(VARCHAR(100))
    comments_count = Column(INTEGER)
    go_detail_count = Column(INTEGER)
    gallary_image_count = Column(INTEGER)
    detail_play_effective_count = Column(INTEGER)
    behot_time =Column(DATETIME)
    create_time = Column(DATETIME)
    update_time = Column(DATETIME)

def _init_db():
    DB_CONNECT_VARCHAR = 'mysql+pymysql://' + config.dbuser + ':' + config.dbpassword + '@' + config.dbhost + ':3306/' + config.dbname + "?charset=utf8mb4"
    engine = create_engine(DB_CONNECT_VARCHAR, echo=False)
    DB_Session = sessionmaker(bind=engine)
    dbsession = DB_Session()
    return dbsession