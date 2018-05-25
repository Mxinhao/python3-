#-*-coding:utf-8-*-
import  scrapy
from selenium import webdriver
import time
import datetime
import json
from tutorial.items import *
from tutorial.account import toutiao_userid
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码


class toutiao(scrapy.Spider):
    name = 'toutiao'
    today = datetime.date.today()
    def __init__(self):
        self.page_num = 200
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
        super(toutiao, self).__init__()
        self.driver = webdriver.PhantomJS()  # desired_capabilities=dcap
        time.sleep(2)
        self.driver.get("https://www.toutiao.com/")

    def start_requests(self):
        for name in toutiao_userid:
            max_behot_time = 0
            user_id=toutiao_userid[name]
            signature=self.get_signature(user_id,max_behot_time)
            article_url = "https://www.toutiao.com/c/user/article/?page_type=1&user_id=" + user_id + "&max_behot_time=" + str(
                max_behot_time) + "&count=" + str(self.page_num) + "&_signature=" + signature
            yield scrapy.Request(article_url,headers=self.headers,meta={"user_id":user_id,"name":name},callback=self.parse_items)
        self.driver.quit()
    def parse_items(self,response):
        user_id=response.meta['user_id']
        name = response.meta['name']
        data = response.text
        arti_data = json.loads(data)
        if arti_data["message"]=="error":
            article_url=response.url
            art_req = scrapy.Request(article_url, headers=self.headers,dont_filter=True, meta={"user_id": user_id,"name":name},
                                     callback=self.parse_items)
            yield art_req
        if arti_data["message"] == "success":
            if 'data' in arti_data:
                print ("article count:%d" % len(arti_data['data']))
                for article in arti_data['data']:
                    new_ToutiaoArticleList = c_toutiao_list_Item()
                    new_ToutiaoArticleList["id"] = article['item_id']
                    new_ToutiaoArticleList["mp_name"] = name
                    new_ToutiaoArticleList["source"] = article['source']
                    new_ToutiaoArticleList["image_url"] = str(article['image_url']) if 'image_url' in article else ''
                    new_ToutiaoArticleList["single_mode"] = article['single_mode']
                    new_ToutiaoArticleList["abstract"] = article['abstract']
                    new_ToutiaoArticleList["title"] = article['title']
                    new_ToutiaoArticleList["image_list"] = '' if article['image_list'] == '[]' else str(article['image_list'])
                    new_ToutiaoArticleList["more_mode"] = article['more_mode']
                    new_ToutiaoArticleList["tag"] = article['tag']
                    new_ToutiaoArticleList["tag_url"] = article['tag_url']
                    new_ToutiaoArticleList["chinese_tag"] = str(article['chinese_tag']) if 'chinese_tag' in article else ''
                    new_ToutiaoArticleList["group_source"] = article['group_source']
                    new_ToutiaoArticleList["comments_count"] = article['comments_count']
                    new_ToutiaoArticleList["media_url"] = str(article['media_url']) if 'media_url' in article else ''
                    new_ToutiaoArticleList["media_avatar_url"] = article[
                        'media_avatar_url'] if 'media_avatar_url' in article else ''
                    new_ToutiaoArticleList["go_detail_count"] = article['go_detail_count']
                    new_ToutiaoArticleList["middle_mode"] = article['middle_mode']
                    new_ToutiaoArticleList["gallary_image_count"] = article['gallary_image_count']
                    new_ToutiaoArticleList["detail_play_effective_count"] = article['detail_play_effective_count']
                    new_ToutiaoArticleList["video_duration_str"] = article[
                        'video_duration_str'] if 'video_duration_str' in article else ''
                    new_ToutiaoArticleList["source_url"] = article['source_url']
                    new_ToutiaoArticleList["article_genre"] = article['article_genre']
                    new_ToutiaoArticleList["display_url"] = article['display_url'] if 'display_url' in article else ''
                    new_ToutiaoArticleList["behot_time"] = str(datetime.datetime.fromtimestamp(article['behot_time']))
                    new_ToutiaoArticleList["has_gallery"] = article['has_gallery']
                    new_ToutiaoArticleList["group_id"] = article['group_id']
                    new_ToutiaoArticleList["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    new_ToutiaoArticleList["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    yield new_ToutiaoArticleList
    def get_signature(self,user_id,max_behot_time):
        time.sleep(1)
        self.driver.get("https://www.toutiao.com/c/user/"+user_id+"/")
        time.sleep(1)
        signature_js = "return TAC.sign(" + user_id + str(max_behot_time) + ");"
        signature = self.driver.execute_script(signature_js)
        return signature
if __name__=="__main__":
    os.system("scrapy crawl toutiao")
    print("------------爬取结束----------------------")