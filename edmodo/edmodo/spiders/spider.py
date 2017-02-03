import scrapy
import time
from selenium import webdriver
from edmodo.items import EdmodoItem
from scrapy.exceptions import DropItem


class edmodoSpider(scrapy.Spider):
    name = "edmodo"
    allowed_domains = ["support.edmodo.com"]
    start_urls = ["https://support.edmodo.com/hc/en-us/categories/200331474"]

    def __init__(self, *args, **kwargs):
        super(edmodoSpider, self).__init__(*args, **kwargs)
        self.driver = webdriver.Chrome(executable_path="F:\Software\chromedriver_win32\chromedriver.exe")


    def parse(self, response):
        self.driver.get(response.url)
        #time.sleep(5)
        for sel in self.driver.find_elements_by_xpath(".//*[@class='library-section-container bottom-library-container']/div"):
            for category in sel.find_elements_by_xpath("ul/li"):
                category.click()
                time.sleep(3)
                for sub_category in category.find_elements_by_xpath("ul/li"):
                    if ("See" not in sub_category.text):
                        sub_category.click()
        contents = scrapy.selector.Selector(text=self.driver.page_source)
        self.driver.close()
        for content in contents.xpath(".//*[@class='library-section-container bottom-library-container']/div"):
            for category in content.xpath('ul/li'):
                item = EdmodoItem()
                print "Category: " + category.xpath('text()').extract()[0]
                item["Category"] = category.xpath('text()').extract()[0]
                for subCategory in category.xpath('ul/li'):
                        try :
                            if ("See" not in subCategory.xpath('text()').extract()[0]):
                                print "Sub_Category: " + subCategory.xpath('text()').extract()[0]
                                item['Sub_category'] = subCategory.xpath('text()').extract()[0]
                            for title in subCategory.xpath("ul/li"):
                                print "Title: "+title.xpath('a/text()').extract()[0]
                                url = title.xpath("a/@href").extract()[0]
                                url = "https://support.edmodo.com" + url.replace('/hc/', '/hc/en-us/')
                                request = scrapy.Request(url, callback=self.getPageInfo)
                                request.meta['item'] = item
                                yield request
                        except IndexError:
                            continue

    def getPageInfo(self, response):
        item = response.meta['item']
        try:
            item["Content_Link"] = response.url
            item["Title"] = response.xpath('.//*[@class="article-column"]/article/h1/text()').extract()[0]
            contents = response.xpath(".//*[@class='article-body markdown']//*/text()").extract()
            longString = ""
            for content in contents:
                longString = longString+" "+content.encode("ascii", "ignore").strip()
            item["Content"] = longString
            return item
        except IndexError:
            DropItem(item)
