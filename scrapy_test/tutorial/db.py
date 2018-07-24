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

class ToutiaoArticleListAPP(Base):
    __tablename__ = 'c_toutiao_list_app_item'
    id = Column(BIGINT, primary_key=True)
    screen_name = Column(VARCHAR(30))
    user_id = Column(BIGINT)
    description = Column(VARCHAR(300))
    avatar_url = Column(VARCHAR(300))
    source = Column(VARCHAR(30))
    title = Column(VARCHAR(300))
    group_id = Column(BIGINT)
    delete = Column(TINYINT)
    media_type = Column(TINYINT)
    forward_count = Column(INTEGER)
    create_time = Column(DATETIME)
    modify_time = Column(DATETIME)
    read_count = Column(INTEGER)
    digg_count = Column(INTEGER)
    is_repost = Column(TINYINT)
    comment_count = Column(INTEGER)

def _init_db():
    DB_CONNECT_VARCHAR = 'mysql+pymysql://' + config.dbuser + ':' + config.dbpassword + '@' + config.dbhost + ':3306/' + config.dbname + "?charset=utf8mb4"
    engine = create_engine(DB_CONNECT_VARCHAR, echo=False)
    DB_Session = sessionmaker(bind=engine)
    dbsession = DB_Session()
    return dbsession