from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from Scrapy.items import ScrapyItem

class ScrapySpider(BaseSpider):
	name = "ss"
	allowed_domains = ["scrapy.org"]
	start_urls = ["https://scrapy.org/"]

	def parse(self, reponse):
		sel = Selector (reponse)
		item = ScrapyItem()
		item["Heading"] = sel.xpath('/html/body/div[2]/div/div[1]/div/div[2]/div/div[2]/p/text()').extract()
		item["Content"] = sel.xpath('/html/body/div[2]/div/div[1]/div/div[1]/p[1]/text()').extract()
		item["Source_Website"] = "https://scrapy.org/"
		return item