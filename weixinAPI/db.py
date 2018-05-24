# -*-coding:utf-8-*-
# !/usr/bin/python
import pymysql
import config

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

class WeiXinCropArticle(Base):
	__tablename__ = 'weixin_corp_article'
	id = Column(BIGINT, primary_key=True,autoincrement=True)
	name=Column(VARCHAR(255))
	ref_date = Column(DATE)
	msgid = Column(VARCHAR(12))
	msgid_serial=Column(VARCHAR(12))
	msgid_sort = Column(INTEGER)
	title=Column(TEXT)
	stat_date = Column(DATE)
	stat_sort = Column(INTEGER)
	target_user = Column(INTEGER)
	int_page_read_user = Column(INTEGER)
	int_page_read_count = Column(INTEGER)
	ori_page_read_user = Column(INTEGER)
	ori_page_read_count = Column(INTEGER)
	share_user = Column(INTEGER)
	share_count = Column(INTEGER)
	add_to_fav_user = Column(INTEGER)
	add_to_fav_count = Column(TINYINT)
	int_page_from_session_read_user = Column(INTEGER)
	int_page_from_session_read_count = Column(INTEGER)
	int_page_from_hist_msg_read_user = Column(INTEGER)
	int_page_from_hist_msg_read_count = Column(INTEGER)
	int_page_from_feed_read_user = Column(INTEGER)
	int_page_from_feed_read_count = Column(INTEGER)
	int_page_from_friends_read_user = Column(INTEGER)
	int_page_from_friends_read_count = Column(INTEGER)
	int_page_from_other_read_user = Column(INTEGER)
	int_page_from_other_read_count = Column(INTEGER)
	feed_share_from_session_user = Column(INTEGER)
	feed_share_from_session_cnt = Column(INTEGER)
	feed_share_from_feed_user = Column(INTEGER)
	feed_share_from_feed_cnt = Column(INTEGER)
	feed_share_from_other_user = Column(INTEGER)
	feed_share_from_other_cnt = Column(INTEGER)

class WeiXinCorpInfo(Base):
	__tablename__="weixin_corp_info"
	id = Column(BIGINT,primary_key=True,autoincrement=True)
	type=Column(VARCHAR(15))
	brand = Column(VARCHAR(30))
	name = Column(VARCHAR(255))
	original_id = Column(VARCHAR(255))
	weixin_id=Column(VARCHAR(255))
	username=Column(VARCHAR(255))
	password = Column(VARCHAR(255))
	company=Column(VARCHAR(255))
	appid=Column(VARCHAR(255))
	appsecret=Column(VARCHAR(255))
	follows=Column(INTEGER)
	authed=Column(INTEGER,default=1)
	enabled=Column(INTEGER,default=1)
	update_time=Column(DATETIME)
	access_token=Column(VARCHAR(256))
	expire_time=Column(DATETIME)

class WeiXinFollowersHistory(Base):
	__tablename__ = "weixin_followers_history"
	id=Column(BIGINT,primary_key=True,autoincrement=True)
	name=Column(VARCHAR(255))
	new_user=Column(INTEGER)
	cancel_user=Column(INTEGER)
	cumulate_user=Column(INTEGER)
	update_time=Column(DATETIME)
	ref_date=Column(DATE)

class WeiXinArticleContent(Base):
	__tablename__ = "weixin_article_content"
	id=Column(BIGINT,primary_key=True)
	media_id=Column(VARCHAR(255))
	media_sort=Column(VARCHAR(255))
	mp_name=Column(VARCHAR(255))
	title=Column(VARCHAR(255))
	author=Column(VARCHAR(255))
	digest=Column(VARCHAR(255))
	content=Column(VARCHAR(255))
	content_source_url=Column(VARCHAR(255))
	thumb_media_id=Column(VARCHAR(255))
	show_cover_pic=Column(VARCHAR(255))
	url=Column(VARCHAR(255))
	thumb_url=Column(VARCHAR(255))
	create_time=Column(DATETIME)
	update_time=Column(DATETIME)

def _init_db():
	DB_CONNECT_VARCHAR = 'mysql+pymysql://' + config.dbuser + ':' + config.dbpassword + '@' + config.dbhost + ':3306/' + config.dbname + "?charset=utf8mb4"
	engine = create_engine(DB_CONNECT_VARCHAR, echo=False)
	DB_Session = sessionmaker(bind=engine)
	dbsession = DB_Session()
	return dbsession
dbsession=_init_db()