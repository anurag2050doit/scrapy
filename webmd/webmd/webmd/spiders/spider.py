#Author: Anurag Misra
#Date: 12/16/2016
#Organization: Thought Toast
#Purpose: To extract the disease and there discription from webmd pages.


import scrapy

from webmd.items import WebmdItem

class webmdSpider(scrapy.Spider):
	name = "webmd"
	allowed_domains = ["webmd.com"]
	start_urls = ["http://www.webmd.com/a-to-z-guides/common-topics/default.htm"]


	def parse(self, response):
		for sel in response.xpath(".//*[@id='a-z-alpha']/ul/li"):
			pages = sel.xpath("a/@href").extract()
			for page in pages:
				link = "http://www.webmd.com/"+ page
				yield scrapy.Request(link, callback=self.parsePageDetails, method='GET')


	def parsePageDetails(self, response):
		for sel in response.xpath(".//*[@class='a-to-z list']/ul/li"):
			item = WebmdItem()
			item['Category'] = sel.xpath("a/text()").extract()[0]
			link = sel.xpath("a/@href").extract()[0]
			url = "http://www.webmd.com/" + link
			request = scrapy.Request(url, callback=self.getContentInfo)
			request.meta['item'] = item
			yield request


	def getContentInfo(self, response):
		item = response.meta['item']
		item['Content_Link'] = response.url
		print "getContentInfo"
		try:
			if(len(response.xpath('//*[@itemprop="headline"]/text()').extract()) != 0):
				item['Title'] = response.xpath('//*[@itemprop="headline"]/text()').extract()[0]
				lng_string = ""
				contents = response.xpath('//*[@class="article-page active-page"]//*/text()').extract()
				for content in contents:
					string = content.encode('ascii','ignore').strip()
					lng_string = lng_string+" "+string
				item['Content'] = lng_string
			if( len(response.xpath('//*[@class="tb_main"]/text()').extract())!= 0):
				item['Title'] = response.xpath('//*[@class="tb_main"]//*/text()').extract()[0]
				content = response.xpath('//*[@class="teaser_fmt"]/p/text()').extract()[0]
				item['Content'] = content
		except IndexError:
			return
		return item
