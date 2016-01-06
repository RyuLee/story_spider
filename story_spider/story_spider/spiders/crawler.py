# -*- coding:utf-8 -*-
# author: ryulee

import scrapy
from .. import items

class storySpider(scrapy.Spider):
	"""docstring for storySpider"""
	name = "storySpider"
	allowed_domains=['moralstories.org']
	start_urls = [
	"http://www.moralstories.org/education/",
	"http://www.moralstories.org/fables/",
	"http://www.moralstories.org/family/",
	"http://www.moralstories.org/inspiration/",
	"http://www.moralstories.org/life/",
	"http://www.moralstories.org/love/",
	"http://www.moralstories.org/motivation/"
	]

	def parse_contents(self, response):
		for sel in response.xpath('//div[@id = "contents"]'):
			item = items.StorySpiderItem()
			item['title'] = sel.xpath('//div[@class = "title"]/text()').extract()
			item['content'] = sel.xpath('//div[@class = "post"]/div[2]/text()|//div[@class = "post"]/div[2]/p/text()').extract()
			item['moral'] = sel.xpath('//blockquote/text()').extract()
			yield item
	def parse(self,response):
		for href in response.xpath('//h2/a/@href'):
			url = response.urljoin(href.extract())
			#print url
			yield scrapy.Request(url,callback = self.parse_contents)
		next_page = response.xpath('//a[@class = "next page-numbers"]/@href')
		page_counter = 1
		if next_page:
			url = response.urljoin(next_page[0].extract())
			print url
			page_counter = page_counter+1
			yield scrapy.Request(url,callback = self.parse)

class proverbSpider(scrapy.Spider):
	name = "proverbSpider"
	allowed_domains = ['wiki.quote.org']
	start_urls = ['https://en.wikiquote.org/wiki/English_proverbs_(alphabetically_by_proverb)']

	def parse(self,response):
		for sel in response.xpath('//div[@id = "mw-content-text"]/ul'):
			item = items.ProverbSpiderItem()
			item['content'] = sel.xpath('/li/text()').extract()
			item['note'] = sel.xpath('/li/ul/li[contains(text(),"Note")]').extract()
			item['meaning'] = sel.xpath('/li/ul/li[contains(text(),"Meaning")]').extract()
			yield item
		