#-*-coding:utf-8-*-
from tutorial.items import *
from tutorial.db import *
# 将scrapy的item转换为sqlachemy的ORM的数据库类
class itemToDB():
    def __init__(self):
        super()
    def cover(self,item,db):
        backDB=db()
        item_dict=item.__dict__
        db_dict=db.__dict__
        for key,value in db_dict.items():
            if key in item_dict["_values"]:
                backDB.__setattr__(key,item_dict["_values"][key])
        return backDB