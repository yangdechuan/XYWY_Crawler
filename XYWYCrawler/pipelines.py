# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from XYWYCrawler.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_collections

class XywycrawlerPipeline(object):
    def open_spider(self, spider):
        self.host = mongo_host
        self.port = mongo_port
        self.dbname = mongo_db_name
        self.sheetname = mongo_db_collections
        self.client = pymongo.MongoClient(self.host, port=self.port)
        self.mydb = self.client[self.dbname]
        self.post = self.mydb[self.sheetname]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
