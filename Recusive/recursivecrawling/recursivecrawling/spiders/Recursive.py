from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from recursivecrawling.items import RecursivecrawlingItem


class RecursiveScrapySpider(CrawlSpider):
	name = "rs"
	allowed_domains = ["cse.iitd.ernet.in"]
	start_urls = ["http://cse.iitd.ernet.in/~naveen"]

	rules = (
		Rule(SgmlLinkExtractor(allow=("cse\.iitd\.ernet\.in/\~naveen/.*")), callback='parse_item', follow=True),
		)

	def parse_item(self, response):
		sel = Selector(response)
		item = RecursivecrawlingItem()
		item ["URL"] = response.request.url
		item["content"] = sel.xpath('/html/body/table/tbody/tr[3]/td[1]/text()[1]').extract()
		return item