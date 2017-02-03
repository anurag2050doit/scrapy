# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuickbooksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category = scrapy.Field()
    SubCategory = scrapy.Field()
    Title = scrapy.Field()
    ContentURL = scrapy.Field()
    Content = scrapy.Field()
#    visit_id = scrapy.Field()
#    visit_status = scrapy.Field()
    pass
