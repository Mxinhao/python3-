# -*-coding:utf-8-*-
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

class WeiBoArticleList(Base):
	__tablename__ = 'weibo_api_article_list'
	mp_name = Column(VARCHAR(30), primary_key=True)
	created_at = Column(DATETIME)
	update_at = Column(DATETIME)
	id = Column(BIGINT, primary_key=True)
	text=Column(TEXT)
	idstr = Column(BIGINT)
	mid = Column(BIGINT)
	can_edit=Column(TINYINT)
	textLength=Column(INTEGER)
	source_allowclick=Column(INTEGER)
	source_type=Column(INTEGER)
	source=Column(VARCHAR(255))
	favorited=Column(TINYINT)
	truncated=Column(TINYINT)
	in_reply_to_status_id=Column(VARCHAR(32))
	in_reply_to_user_id=Column(VARCHAR(32))
	in_reply_to_screen_name=Column(VARCHAR(255))
	thumbnail_pic=Column(VARCHAR(300))
	bmiddle_pic=Column(VARCHAR(300))
	original_pic=Column(VARCHAR(300))
	geo=Column(TEXT)
	retweeted_status=Column(TEXT)
	reposts_count=Column(INTEGER)
	comments_count=Column(INTEGER)
	attitudes_count=Column(INTEGER)
	mlevel=Column(INTEGER)
	visible=Column(TEXT)
	pic_ids=Column(TEXT)
	user=Column(TEXT)

class WeiBoInfo(Base):
	__tablename__="weibo_api_info"
	uid = Column(BIGINT,primary_key=True)
	mp_name = Column(VARCHAR(50))
	url = Column(VARCHAR(200))
	brand=Column(VARCHAR(30))
	type=Column(VARCHAR(30))
	appid=Column(VARCHAR(20))
	appsecrpt=Column(VARCHAR(50))
	access_token=Column(VARCHAR(50))
	callback_url=Column(VARCHAR(50))
	username=Column(VARCHAR(255))
	password=Column(VARCHAR(255))
	expitrs=Column(BIGINT)
	description=Column(VARCHAR(300))
	containerid=Column(BIGINT)
	updated=Column(DATETIME)
	enabled=Column(TINYINT)


class WeiBoAPIComment(Base):
	__tablename__="weibo_api_comment"
	id = Column(BIGINT,primary_key=True)
	rootid=Column(BIGINT)
	floor_number=Column(INTEGER)
	text = Column(TEXT)
	created_at=Column(DATETIME)
	source=Column(VARCHAR(255))
	user_id=Column(BIGINT)
	mid=Column(VARCHAR(30))
	idstr=Column(VARCHAR(30))
	reply_comment=Column(VARCHAR(30))
	weibo_id=Column(BIGINT)
class WeiBoAPIFollowers(Base):
	__tablename__="weibo_api_followers"
	id = Column(BIGINT,primary_key=True)
	weibo_id=Column(BIGINT)
	mp_name=Column(VARCHAR(30))
	followers_count=Column(INTEGER)
	friends_count=Column(INTEGER)
	statuses_count=Column(INTEGER)
	update_time=Column(DATETIME)

class WeiBoAPIUserinfo(Base):
	__tablename__="weibo_api_userinfo"
	id = Column(BIGINT,primary_key=True)
	idstr = Column(VARCHAR(30))
	screen_name=Column(VARCHAR(50))
	name=Column(VARCHAR(50))
	province=Column(INTEGER)
	city=Column(INTEGER)
	location = Column(VARCHAR(30))
	description=Column(VARCHAR(255))
	profile_image_url=Column(VARCHAR(300))
	url=Column(VARCHAR(300))
	profile_url=Column(VARCHAR(300))
	domain=Column(VARCHAR(300))
	weihao=Column(VARCHAR(300))
	gender=Column(VARCHAR(5))
	followers_count=Column(INTEGER)
	friends_count=Column(INTEGER)
	statuses_count=Column(INTEGER)
	favourites_count=Column(INTEGER)
	created_at=Column(DATETIME)
	allow_all_act_msg=Column(TINYINT)
	geo_enabled=Column(TINYINT)
	verified=Column(TINYINT)
	remark=Column(VARCHAR(30))
	verified_type=Column(INTEGER)
	following=Column(TINYINT)
	status_id=Column(INTEGER)
	allow_all_comment=Column(TINYINT)
	avatar_large=Column(VARCHAR(300))
	avatar_hd=Column(VARCHAR(300))
	verified_reason=Column(VARCHAR(255))
	follow_me=Column(TINYINT)
	online_status=Column(INTEGER)
	bi_followers_count=Column(INTEGER)
	lang=Column(VARCHAR(10))



def _init_db():
	DB_CONNECT_VARCHAR = 'mysql+pymysql://' + config.dbuser + ':' + config.dbpassword + '@' + config.dbhost + ':3306/' + config.dbname + "?charset=utf8mb4"
	engine = create_engine(DB_CONNECT_VARCHAR, echo=False)
	DB_Session = sessionmaker(bind=engine)
	dbsession = DB_Session()
	return dbsession
dbsession=_init_db()