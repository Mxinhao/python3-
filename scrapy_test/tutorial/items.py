# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class c_toutiao_list_app_item(scrapy.Item):
    id = scrapy.Field()
    screen_name = scrapy.Field()
    user_id= scrapy.Field()
    description=scrapy.Field()
    avatar_url=scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    group_id = scrapy.Field()
    delete = scrapy.Field()
    media_type = scrapy.Field()
    forward_count = scrapy.Field()
    create_time = scrapy.Field()
    modify_time = scrapy.Field()
    read_count = scrapy.Field()
    digg_count = scrapy.Field()
    is_repost = scrapy.Field()
    comment_count = scrapy.Field()