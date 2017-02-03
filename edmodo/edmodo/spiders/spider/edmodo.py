import scrapy
import time
from elasticsearch import Elasticsearch
#import os
from selenium import webdriver
from items import EdmodoItem
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
es = Elasticsearch()


def parse3():
    yield "1"

class edmodoSpider(scrapy.Spider):
    name = "edmodo"
    allowed_domains = ["support.edmodo.com"]
    #start_urls = ["https://support.edmodo.com/hc/en-us/categories/200331474"]

    def __init__(self, *args, **kwargs):
        #super(edmodoSpider, self).__init__(*args, **kwargs)
        #self.download_delay = 0.25
        #self.driver = webdriver.Chrome("F:\Software\chromedriver_win32\chromedriver.exe")
        #binary = FirefoxBinary("C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")
        #caps = DesiredCapabilities.FIREFOX
        #caps["marionette"] = True
        #caps["binary"] = "C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe"
        #fireFoxdriver = "D:\Scrapy Projects\scrapy\scrapy\edmodo\edmodo\spiders\geckodriver.exe"
        #browser = webdriver.Firefox(capabilities=caps,executable_path=fireFoxdriver)

        #self.browser = webdriver.Chrome(executable_path="F:\Software\chromedriver_win32\chromedriver.exe")
        #self.browser
        #os.environ["webdriver.gecko.driver"] = fireFoxdriver
        #webdriver.chrome.driver = "F:\Software\chromedriver_win32\chromedriver.exe"
        #self.browser = webdriver.Firefox()
        #self.browser = webdriver.Remote(
        #    desired_capabilities={'browserName': 'Firefox',
        #                           'moz:firefoxOptions.binary': "D:\Scrapy Projects\scrapy\scrapy\edmodo\edmodo\spiders\geckodriver.exe"})
            #self.browser = webdriver.Firefox()
        #self.browser.implicitly_wait(100)
        #ed = edmodoSpider()
        print "anurag"
        #self.parse2()
        #self.brower.maximize_window()

    def parse2(self):
        print "anuragX"
        browser = webdriver.Chrome(executable_path="F:\Software\chromedriver_win32\chromedriver.exe")

        browser.get("https://support.edmodo.com/hc/en-us/categories/200331474")
        result = {}
        for sel in browser.find_elements_by_xpath(".//*[@class='library-section-container bottom-library-container']/div"):
            for category in sel.find_elements_by_xpath("ul/li"):
                category.click()
                time.sleep(2)
                for sub_category in category.find_elements_by_xpath("ul/li"):
                    sub_category.click()
                    time.sleep(1)
                break
        content = scrapy.selector.Selector(text=browser.page_source)
        browser.close()
        #for sel in content.xpath(".//*[@class='library-section-container bottom-library-container']/div"):
        categories = content.xpath(".//*[@class='library-section-container bottom-library-container']/div/ul/li")
        #categories.extract(

        for category in categories:
            item = EdmodoItem()
            item["Category"] = category.xpath("text()").extract()[0]
            #subCategories = category.xpath("ul/li");
            #subCategories.extract()
        for sub_category in content.xpath(".//*[@class='library-section-container bottom-library-container']/div/ul/li/ul/li/text()"):
            item["Sub_category"] = sub_category.extract()
            #if (sub_category.xpath(''))
            #titles = sub_category.xpath("ul/li");
        for title in content.xpath(".//*[@class='library-section-container bottom-library-container']/div/ul/li/ul/li/ul/li/a"):
            link = "https://support.edmodo.com" + title.xpath("@href").extract()[0]
            item['Content_Link'] = link
            titleText = title.xpath("text()").extract()[0]
            item['Title'] = titleText
            #pr
            request = scrapy.Request(link, callback=self.getContentInfo)
            request.meta["item"] = item
            #yield 1

            yield request


    def parsePageDetails(self, response):
        item = response.meta['item']
        item = self.getContentInfo(item, response)
        print "---------------"
        print item
        return item

    def getContentInfo(self , response):
        item = response.meta['item']
        contents = response.xpath(".//*[@class='article-body markdown']//*/text()").extract()
        lng_string = ""
        for content in contents:
				string = content.encode('ascii','ignore').strip()
				lng_string = lng_string+" "+string
        item["Content"] = lng_string

        yield item

edmodos = edmodoSpider()
list(edmodos.parse2())
