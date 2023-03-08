# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.books_phsy


    def process_item(self, item, spider):

        item['name'] = self.process_name_book(item['name'])
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_name_book(self, name):
        name = name.replace('Аннотация к книге', '')

        return name