# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tutorial.items import *
from tutorial.db import ToutiaoArticleList,ToutiaoArticleHistory,_init_db
import datetime
import time
from tutorial.itemToDB import itemToDB
itemToDB=itemToDB()
today=time.strftime('%Y-%m-%d', time.localtime())
time_interval=int(time.strftime('%H', time.localtime()))
time_interval_history=[0,6,9,12,15,18,20,22]
time_interval_current=[6,9,12,15,18,20,22]

class ToutiaoPipeline(object):
    def __init__(self):
        self.dbsession = _init_db()
    def process_item(self,item,spider):
        if  isinstance(item,c_toutiao_list_Item):
            # item对象转为SQlchemy 的映射对象
            article=itemToDB.cover(item,ToutiaoArticleList)
            result_check = self.dbsession.query(ToutiaoArticleList).filter(ToutiaoArticleList.id == article.id)
            if result_check.count():
                del article.create_time
                self.dbsession.merge(article)
                self.dbsession.commit()
                print("update article:" + article.title)
            else:
                self.dbsession.add(article)
                self.dbsession.commit()
            if time_interval in time_interval_history:
                row_count = self.dbsession.query(ToutiaoArticleHistory).filter(ToutiaoArticleHistory.id == item['id'],
                                                               ToutiaoArticleHistory.type == 'history').count()
                new_ToutiaoArticleHistory = ToutiaoArticleHistory()
                new_ToutiaoArticleHistory.id = item['id']
                new_ToutiaoArticleHistory.sort = row_count + 1
                new_ToutiaoArticleHistory.type = 'history'
                new_ToutiaoArticleHistory.mp_name = item["mp_name"]
                new_ToutiaoArticleHistory.source = item['source']
                new_ToutiaoArticleHistory.title = item['title']
                new_ToutiaoArticleHistory.chinese_tag = str(item['chinese_tag']) if 'chinese_tag' in item else ''
                new_ToutiaoArticleHistory.comments_count = item['comments_count']
                new_ToutiaoArticleHistory.go_detail_count = item['go_detail_count']
                new_ToutiaoArticleHistory.gallary_image_count = item['gallary_image_count']
                new_ToutiaoArticleHistory.detail_play_effective_count = item['detail_play_effective_count']
                new_ToutiaoArticleHistory.behot_time = item['behot_time']
                new_ToutiaoArticleHistory.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                new_ToutiaoArticleHistory.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                self.dbsession.merge(new_ToutiaoArticleHistory)
                self.dbsession.commit()

                print("add history article:" + new_ToutiaoArticleHistory.title)

            if time_interval in time_interval_current and today == item['behot_time'][:10]:
                row_count = self.dbsession.query(ToutiaoArticleHistory).filter(ToutiaoArticleHistory.id == item['id'],
                                                               ToutiaoArticleHistory.type == 'today').count()
                new_ToutiaoArticleHistory = ToutiaoArticleHistory()
                new_ToutiaoArticleHistory.id = item['id']
                new_ToutiaoArticleHistory.sort = row_count + 1
                new_ToutiaoArticleHistory.type = 'today'
                new_ToutiaoArticleHistory.mp_name = item["mp_name"]
                new_ToutiaoArticleHistory.source = item['source']
                new_ToutiaoArticleHistory.title = item['title']
                new_ToutiaoArticleHistory.chinese_tag = str(
                    item['chinese_tag']) if 'chinese_tag' in item else ''
                new_ToutiaoArticleHistory.comments_count = item['comments_count']
                new_ToutiaoArticleHistory.go_detail_count = item['go_detail_count']
                new_ToutiaoArticleHistory.gallary_image_count = item['gallary_image_count']
                new_ToutiaoArticleHistory.detail_play_effective_count = item['detail_play_effective_count']
                new_ToutiaoArticleHistory.behot_time = item['behot_time']
                new_ToutiaoArticleHistory.create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                new_ToutiaoArticleHistory.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                self.dbsession.merge(new_ToutiaoArticleHistory)
                self.dbsession.commit()
            return item