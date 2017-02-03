#Author: Anurag Misra
#Date: 12/16/2016
#Organization: Thought Toast
#Purpose: To extract the questions and answer of levis support page.

import scrapy
from levis.items import LevisItem

class LevisSpider(scrapy.Spider):
	name = "levis"
	allowed_domains = ["levi.com/"]
	start_urls = ["http://www.levi.com/US/en_US/customer-service"]

	def parse(self, response):
		i = 2
		while(True):
			item = LevisItem()
			try:
				item["Category"] = response.xpath(".//*[@class='left-cont help-tab show']/div["+ str(i) +"]/div[1]/text()").extract()[0]
			except IndexError:
			    break

			j = 2
			while(True):
				try:
					item["Title"] = response.xpath(".//*[@class='left-cont help-tab show']/div["+ str(i) + "]/div["+ str(j) + "]/ul/li/div[1]/div[3]/text()").extract()[0]
					contents = response.xpath(".//*[@class='left-cont help-tab show']/div["+ str(i) + "]/div["+ str(j) + "]/ul/li/div[2]//*/text()").extract()
					lng_string = ""
					for content in contents:
						string = content.encode('ascii','ignore').strip()
						lng_string = lng_string+" "+string
					item['Content'] = lng_string

				except IndexError:
					break
				j += 1
				yield item
			i += 1
