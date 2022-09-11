# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis
import pymongo
import logging
from Gotspider2.items import Gotspider2Item
import Gotspider2.settings as settings
from urllib import request
from bs4 import BeautifulSoup

class Gotspider2Pipeline(object):
    def process_item(self, item, spider):
        client = pymongo.MongoClient("localhost",27017)
        db = client["xsfh"] #连接目标数据库
        chapter_col = db["chapters"] #连接集合
        chapter_col.insert_one({"chapter_name":item['chapter'],"content":item['content'],
        "characters":item['characters'],"url":item['url']})
        return item
