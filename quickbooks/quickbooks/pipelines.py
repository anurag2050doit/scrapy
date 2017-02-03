# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch
from scrapy.exceptions import DropItem
import hashlib
import re

es = Elasticsearch()
class QuickbooksPipeline(object):

    def process_item(self, item, spider):
        Id = hashlib.sha1(item['ContentURL']).hexdigest()
        doc = {
        "Category" : self.stripHTML(item["Category"]),
        "Title" : self.stripHTML(item["Title"]),
        "SubCategory" : self.stripHTML(item["SubCategory"]),
        "Content": self.stripHTML(item["Content"]),
        "Content_Link": self.stripHTML(item["ContentURL"]),
        }
        es.index(index="crawl-quickbook", doc_type="data", id=Id, body=doc )
        #print item

    def stripHTML(self, string):
        tagStripper = MLStripper()
        tagStripper.feed(string)
        parseString = tagStripper.get_data()
        parseSpace = re.sub(' +',' ',parseString.strip())
        return parseSpace.encode('ascii', "ignore")

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
