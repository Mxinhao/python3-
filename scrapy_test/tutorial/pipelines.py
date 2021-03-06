# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.items import *
from tutorial.db import ToutiaoArticleListAPP,_init_db
import datetime
import time
from tutorial.itemToDB import itemToDB
itemToDB=itemToDB()
class ToutiaoPipeline(object):
    def __init__(self):
        self.dbsession = _init_db()
    def process_item(self,item,spider):
         if  isinstance(item,c_toutiao_list_app_item):
            article=itemToDB.cover(item,ToutiaoArticleListAPP)
            result_check = self.dbsession.query(ToutiaoArticleListAPP).filter(ToutiaoArticleListAPP.id == article.id)
            if result_check.count():
                del article.create_time
                self.dbsession.merge(article)
                print("update article:" + article.title)
            else:
                self.dbsession.add(article)

            self.dbsession.commit()
            return item
