# -*- coding: utf-8 -*-
import scrapy
import requests

class SheffieldSpider(scrapy.Spider):
    name = 'Sheffield'
    allowed_domains = ['www.sheffield.ac.uk']
    start_urls = ['https://www.sheffield.ac.uk/postgraduate/research/scholarships/projects']
    #https://www.findaphd.com/connect/common/phd-details.aspx?CAID=3791&LID=348
    #CAID=3791&LID=348
    def parse(self, response):
        # a=requests.get('https://www.sheffield.ac.uk/postgraduate/research/scholarships/projects')
        a=response.xpath('//a//text()').extract()
        print(a)
