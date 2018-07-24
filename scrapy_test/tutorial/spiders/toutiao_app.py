# -*-coding:utf-8-*-
import scrapy
import time
import datetime
import json
from tutorial.items import *
from tutorial.account import toutiao_userid
import os
class toutiao_app(scrapy.Spider):
    name = 'toutiao_app'
    today = datetime.date.today()
    def __init__(self):
        self.page_num = 300
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
        super(toutiao_app, self).__init__()

    def start_requests(self):
        for name in toutiao_userid:
            max_cursor = 0
            user_id = toutiao_userid[name]
            article_url = "http://i.snssdk.com/dongtai/list/v9/?user_id=" + user_id + "&max_cursor=" + str(max_cursor)
            yield scrapy.Request(article_url, headers=self.headers,
                                 meta={"user_id": user_id, "name": name, "max_cursor": max_cursor},
                                 callback=self.parse_items)

    def parse_items(self, response):
        user_id = response.meta['user_id']
        name = response.meta['name']
        data = response.text
        arti_data = json.loads(data)
        if arti_data["message"] == "success":
            if 'data' in arti_data:
                print("article count:%d" % len(arti_data['data']["data"]))
                max_cursor = arti_data['data']["max_cursor"]
                for article in arti_data['data']["data"]:
                    if article["group"] == {}:
                        continue
                    new_ToutiaoArticleList = c_toutiao_list_app_item()
                    new_ToutiaoArticleList["id"] = article['item_id_str']
                    new_ToutiaoArticleList["screen_name"] = article["user"]["screen_name"]
                    new_ToutiaoArticleList["source"] = article["group"]['source']
                    new_ToutiaoArticleList["user_id"] = article["user"]["user_id"]
                    new_ToutiaoArticleList["description"] = article["user"]["description"]
                    new_ToutiaoArticleList["title"] = article["group"]['title']
                    # print(new_ToutiaoArticleList["screen_name"]+" -----  "+new_ToutiaoArticleList["title"])
                    new_ToutiaoArticleList["avatar_url"] = article["user"]["avatar_url"]
                    new_ToutiaoArticleList["group_id"] = article["group"]["group_id"]
                    new_ToutiaoArticleList["delete"] = article["delete"]
                    new_ToutiaoArticleList["media_type"] = article["group"]["media_type"]
                    new_ToutiaoArticleList["forward_count"] = article["forward_count"]
                    new_ToutiaoArticleList["create_time"] = datetime.datetime.fromtimestamp(article["create_time"])
                    new_ToutiaoArticleList["modify_time"] = datetime.datetime.fromtimestamp(article["modify_time"])
                    new_ToutiaoArticleList["read_count"] = article['read_count']
                    new_ToutiaoArticleList["comment_count"] = article['comment_count']
                    new_ToutiaoArticleList["digg_count"] = article['digg_count']
                    new_ToutiaoArticleList["is_repost"] = article["is_repost"]
                    yield new_ToutiaoArticleList
                if max_cursor != 0:
                    article_url = "http://i.snssdk.com/dongtai/list/v9/?user_id=" + user_id + "&max_cursor=" + str(max_cursor)
                    yield scrapy.Request(article_url, headers=self.headers, dont_filter=True,
                                         meta={"user_id": user_id, "name": name, "max_cursor": max_cursor},
                                         callback=self.parse_items)
if __name__ == "__main__":
    os.system("scrapy crawl toutiao_app")
    print("------------爬取结束----------------------")