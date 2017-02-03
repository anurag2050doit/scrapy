# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LevisItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Category = scrapy.Field()
    Title = scrapy.Field()
    Content = scrapy.Field()
