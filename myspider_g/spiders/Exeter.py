# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider_g.items import HooliItem
from myspider_g.hooli_mode import clear_long_text,find_fee_s,find_title
import re
class ExeterSpider(CrawlSpider):
    name = 'Exeter'
    allowed_domains = ['www.exeter.ac.uk']
    start_urls = ['https://www.exeter.ac.uk/postgraduate/all-courses/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="all-courses-A-Z"]//a'),follow=False,callback='parse_item'),
    )

    def parse_item(self, response):
        print('-------------------------------',response.url)
        fee=response.xpath('//div[@id="Fees"]//text()').extract()
        print(fee)
        tuition_fee=find_fee_s(fee)
        print(tuition_fee)