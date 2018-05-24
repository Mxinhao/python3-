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
	__tablename__ = 'weibo_article_list'
	id = Column(BIGINT, primary_key=True)
	url=Column(VARCHAR(200))
	url = Column(VARCHAR(200))
	murl = Column(VARCHAR(200))
	mp_name=Column(VARCHAR(50))
	followers = Column(TINYINT)
	text=Column(TEXT)
	created_at = Column(DATETIME)
	source = Column(VARCHAR(200))
	uid = Column(BIGINT)
	reposts = Column(INTEGER)
	comments = Column(INTEGER)
	likes = Column(INTEGER)
	updated = Column(DATETIME)
	deleted = Column(TINYINT,default=0)
	reads = Column(INTEGER)
	reads_updatetime = Column(DATETIME)
	wenzhi_try_count = Column(TINYINT,default=0)

class WeiBoInfo(Base):
	__tablename__="weibo_info"
	uid = Column(BIGINT,primary_key=True)
	mp_name = Column(VARCHAR(50))
	url = Column(VARCHAR(200))
	description=Column(VARCHAR(300))
	containerid=Column(BIGINT)
	ucontainerid = Column(BIGINT)
	followers=Column(BIGINT)
	updated=Column(DATETIME)
	ishearst=Column(TINYINT)

class WeiBoFollowersHistory(Base):
	__tablename__ = "weibo_followers_history"
	uid=Column(BIGINT,primary_key=True)
	mp_name=Column(VARCHAR(50))
	followers=Column(INTEGER)
	updated=Column(DATETIME)

def _init_db():
	DB_CONNECT_VARCHAR = 'mysql+pymysql://' + config.dbuser + ':' + config.dbpassword + '@' + config.dbhost + ':3306/' + config.dbname + "?charset=utf8mb4"
	engine = create_engine(DB_CONNECT_VARCHAR, echo=False)
	DB_Session = sessionmaker(bind=engine)
	dbsession = DB_Session()
	return dbsession