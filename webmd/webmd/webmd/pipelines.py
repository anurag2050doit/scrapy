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
class WebmdPipeline(object):

    def process_item(self, item, spider):
        if(item["Title"] and item["Category"] and item["Content"] ):
            Id = hashlib.sha1(item["Content_Link"]).hexdigest()
            doc = {
            "Category" : self.stripHTML(item["Category"]),
            "Title" : self.stripHTML(item["Title"]),
            "Content": self.stripHTML(item["Content"]),
            "Content_Link": self.stripHTML(item["Content_Link"]),
            }
            es.index(index="crawl-webmd", doc_type="data", id=Id, body=doc )
        else:
            DropItem(item)

        return item

    def stripHTML(self, string):
        tagStripper = MLStripper()
        tagStripper.feed(string)
        parseString = tagStripper.get_data()
        parseSpace = re.sub(' +',' ',parseString.strip())
        return parseSpace.encode('utf-8', "ignore").replace("®", "")

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
