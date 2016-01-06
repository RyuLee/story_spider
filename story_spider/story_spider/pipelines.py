# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class StorySpiderPipeline(object):

	def __init__(self):
		self.titles_seen = set()
	def process_item(self, item, spider):
		if(item['title'][0] in self.titles_seen):
				raise DropItem("Duplicate item found: %s" % item)
		else:
			self.titles_seen.add(item['title'][0])
			content = str()
			for elem in item['content']:
				elem = elem.encode('utf-8')
				elem = elem.strip(' \t\r\n')
				content = content + elem
			item['content'] = content
			moral = item['moral'][0].encode('utf-8')
			item['moral'] = moral.replace('Moral: ','')
			title = item['title'][0].encode('utf-8')
			title = title.strip(' \t\r\n')
			item['title'] = title
			return item