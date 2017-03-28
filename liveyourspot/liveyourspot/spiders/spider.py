import scrapy

from liveyourspot.items import LiveyourspotItem

class liveyourspotSpider(scrapy.Spider):
    name = "liveyourspot"
    allowed_domains = ["liveyoursport.com"]
    start_urls = ["https://www.liveyoursport.com/tennis/"]

    def parse(self,response):
        for x in xrange(1,78):
            pages = "https://www.liveyoursport.com/tennis/?page="+str(x)
            request = scrapy.Request(pages, callback=self.getContentInfo)
            yield request


    def getContentInfo(self, response):
        for sel in response.xpath("//*[@id='frmCompare']/ul/li"):
            item = LiveyourspotItem()
            price = ""
            try:
                price = sel.xpath("div[3]/em/span/text()").extract()[0]
            except:
                price = sel.xpath("div[3]/em/text()").extract()[0]
            item['price'] = price
            item['product_name'] =  sel.xpath("div[3]/strong/a/text()").extract()[0]
            url = sel.xpath("div[3]/strong/a/@href").extract()[0]
            item['URL'] = url
            request = scrapy.Request(url, callback=self.getDescription)
            request.meta['item'] = item
            yield request

    def getDescription(self, response):
        item = response.meta['item']
        contents = response.xpath("//*[@id='ProductDescription']//*/text()").extract()
        description = ''
        for content in contents:
            string = content.encode('ascii', 'ignore').strip()
            description = description+"/n"+string
        item['description'] = description
        return item
