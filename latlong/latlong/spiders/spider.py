import scrapy
from latlong.items import LatlongItem

class latlongSpider(scrapy.Spider):
    name = "latlong"
    allowed_domains = ["latlong.net"]
    start_urls = ["http://www.latlong.net/category/cities-102-15.html"]

    def parse(self,response):
        for i in range(2,52):
            item = LatlongItem()
            item["Place_Name"] = response.xpath("/html/body/main/div/div[1]/table/tbody/tr["+str(i)+"]/td/a/text()").extract()
            item["Latitude"] = response.xpath("/html/body/main/div/div[1]/table/tbody/tr["+str(i)+"]/td["+str(2)+"]/text()").extract()
            item["Longitude"] = response.xpath("/html/body/main/div/div[1]/table/tbody/tr["+str(i)+"]/td["+str(3)+"]/text()").extract()
            print item
