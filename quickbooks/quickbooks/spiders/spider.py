#Author: Anurag Misra
#Date: 12/16/2016
#Organization: Thought Toast
#Purpose: To extract the articles of quickbooks page.
import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from quickbooks.items import QuickbooksItem

class quickbooksSpider(scrapy.Spider):
    name = "quickbooks"
    allowed_domains = ["community.intuit.com"]
    start_urls = ["https://community.intuit.com/quickbooks-online"]
    archorURL = []
    browseURL = []

    def parse(self, response):
        objs = LinkExtractor(allow=("https://community.intuit.com/browse/.*") , unique=True ).extract_links(response)
        for obj in objs:
            item = QuickbooksItem()
            item["Category"] = obj.text
            request = scrapy.Request(obj.url , callback=self.getContentInfo)
            request.meta['item'] = item
            yield request


    def getContentInfo(self, response):
        item = response.meta['item']
        articles = LinkExtractor(allow=("https://community.intuit.com/articles/.*"), unique=True).extract_links(response)
        for article in articles:
            item["SubCategory"] = article.text
            request = scrapy.Request(article.url, callback=self.getArticleInfo)
            request.meta['item']= item
            yield request

        browses = LinkExtractor(allow=("https://community.intuit.com/browse/.*"), unique=True).extract_links(response)
        for browse in browses:
            request = scrapy.Request(browse.url, callback=self.getContentInfo)
            request.meta['item'] = item
            yield request


    def getArticleInfo(self, response):
        item = response.meta['item']
        item["ContentURL"] = response.url
        contents = response.xpath("/html/body/div[2]/div/div[1]/section[1]//*/text()").extract()
        lng_string = ""
        for content in contents:
            string = content.encode('ascii','ignore').strip()
            lng_string = lng_string+" "+string
        item['Content'] = lng_string
        try :
            titles = response.xpath("/html/body/div[2]/div/div[1]/section[1]/h1/text()").extract()[0]
            item["Title"] = titles
        except IndexError:
            print "===================="
            print "PROBLEM IN THIS PAGE", response.url


        return item
