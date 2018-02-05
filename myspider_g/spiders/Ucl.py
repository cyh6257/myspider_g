# -*- coding: utf-8 -*-
from scrapy.spider import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider_g.items import HooliItem
from myspider_g.hooli_mode import clear_long_text,find_fee_s,find_title


class UclSpider(CrawlSpider):
    name = 'Ucl'
    allowed_domains = ['ucl.ac.uk']
    start_urls = ['http://www.ucl.ac.uk/prospective-students/graduate/research/degrees']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//ul[@id="results"]//tbody//a'),follow=False,callback='parse_item'),
    )


    def parse_item(self, response):
        university="London's Global University"
        print('-------',response.url)
        item=HooliItem()
        programme=response.xpath('//h1[@class="hero__title"]/text()').extract()
        programme=''.join(programme)

        #//section[@class="copy__section copy__section--research"][1]//text()
        overview=response.xpath('//section[@class="copy__section copy__section--research"][1]//text()').extract()
        overview=clear_long_text(overview)
        # print(overview)

        modules=response.xpath('//section[@class="copy__section copy__section--research"][2]//text()').extract()
        modules=clear_long_text(modules)


        longtext=response.xpath('//section[@class="copy__section copy__section--key__information copy__section--research"]//text()').extract()
        tuition_fee=find_fee_s(''.join(longtext))

        if tuition_fee==[]:
            tuition_fee=''

        if 'Programme starts' in longtext:
            start_date=longtext[longtext.index('Programme starts')+2]
        else:
            start_date=''

        if 'Full time:' in longtext:
            mode='Full-time'
            duration=longtext[longtext.index('Full time:')+1]
        else:
            mode=''
            duration=''

        deparments=response.xpath('//section[@class="copy__section copy__section--research"]//text()').extract()
        # print(deparments)
        if 'Department:' in deparments:
            deparment=deparments[deparments.index('Department:')+2]
        else:
            deparment=''

        career=find_title('Careers',deparments)
        career=clear_long_text(career)
        teaching_assessment=find_title('Degree structure',deparments)
        teaching_assessment=clear_long_text(teaching_assessment)

        #中国学术要求
        China_r=["Equivalent qualifications for China Bachelor's degree with a minimum overall average mark of 85%. Please note that a number of programmes / departments will require higher marks. ALTERNATIVE QUALIFICATIONS Medical/ Dental/ Master's degree; Doctorate."]
        entry_requirements=longtext+China_r
        entry_requirements=clear_long_text(entry_requirements)

        item["university"] = university
        item["location"] = ''
        item["department"] = deparment
        item["programme"] = programme
        item["degree_type"] = ''
        item["overview"] = overview
        item["mode"] = mode
        item["IELTS"] = ''
        item["TOEFL"] = ''
        item["teaching_assessment"] = teaching_assessment
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url

        yield item