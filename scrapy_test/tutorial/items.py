# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
class c_toutiao_list_Item(scrapy.Item):
    id = scrapy.Field()
    mp_name = scrapy.Field()
    source = scrapy.Field()
    image_url = scrapy.Field()
    single_mode = scrapy.Field()
    abstract = scrapy.Field()
    title = scrapy.Field()
    image_list = scrapy.Field()
    more_mode = scrapy.Field()
    tag = scrapy.Field()
    tag_url = scrapy.Field()
    chinese_tag = scrapy.Field()
    group_source = scrapy.Field()
    comments_count = scrapy.Field()
    media_url = scrapy.Field()
    media_avatar_url = scrapy.Field()
    go_detail_count = scrapy.Field()
    middle_mode = scrapy.Field()
    gallary_image_count = scrapy.Field()
    detail_play_effective_count = scrapy.Field()
    video_duration_str = scrapy.Field()
    source_url = scrapy.Field()
    article_genre = scrapy.Field()
    display_url = scrapy.Field()
    behot_time = scrapy.Field()
    has_gallery = scrapy.Field()
    group_id = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()