# -*- coding: utf-8 -*-
from myspider_g.hooli_mode import find_title,find_fee_s,index_1
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from myspider_g.hooli_mode import clear_long_text
from myspider_g.items import HooliItem
import re
class DurSpider(CrawlSpider):
    name = 'Dur'
    allowed_domains = ['dur.ac.uk']
    start_urls = ['https://www.dur.ac.uk/courses/all/']

    rules = (
        Rule(LinkExtractor(allow=(r'https://www.dur.ac.uk/courses/info/.*'),restrict_xpaths=('//table//a')),follow=False,callback='parse_item'),
    )
    # r = requests.get('https://www.dur.ac.uk/courses/all/')
    # print(r.content)
    def parse_item(self, response):
        print('---------------------',response.url)
        item=HooliItem()
        programme=response.xpath('//div[@id="course"]/div[@class="row-fluid titlebar"]/h1/span[@class="span7 title"]/text()').extract()
        programme=clear_long_text(programme)
        # print(programme)
        degree_type=response.xpath('//div[@id="course"]/div[@class="row-fluid titlebar"]/h1//span[@class="type"]/text()').extract()
        degree_type=clear_long_text(degree_type)
        # print(degree_type)
        #//div[@id="essentials"]//text()
        essentials=response.xpath('//div[@id="essentials"]//text()').extract()
        # print(essentials)
        ucas_code=index_1('UCAS code',essentials,2)
        mode=index_1('Mode of study',essentials,2)
        duration=index_1('Duration',essentials,2)
        Alevel=index_1('A-Level',essentials,4)
        IB=index_1('International Baccalaureate',essentials,4)
        location=index_1('Location',essentials,3).strip()

        feesfunding=response.xpath('//div[@id="feesfunding"]//text()').extract()
        tuition_fee=find_fee_s(feesfunding)
        if tuition_fee==[]:
            tuition_fee=''.join(tuition_fee)

        coursecontent=response.xpath('//div[@id="coursecontent"]//text()').extract()
        overview=clear_long_text(coursecontent)

        #learning
        teaching_assessment=response.xpath('//div[@id="coursecontent"]//text()').extract()
        teaching_assessment=clear_long_text(teaching_assessment)

        entry_requirements=response.xpath('//div[@id="admissions"]//text()').extract()
        entry_requirements=clear_long_text(entry_requirements)
        IELTS=re.findall('IELTS[\s]*\d.\d[\s\(\w]*',entry_requirements)
        IELTS=''.join(IELTS)
        # print(IELTS)
        #opportunities
        career=response.xpath('//div[@id="opportunities"]//text()').extract()
        career=clear_long_text(career)
        department=response.xpath('//div[@id="department"]/h3/text()').extract()
        department=''.join(department)
        modules=response.xpath('//div[@id="coursecontent"]//text()').extract()
        modules=clear_long_text(modules)

        if degree_type not in ['BA','BEng','BSc','PCert','PGCE','GDip','LLB']:
            # print(degree_type)
            university='Durham University'
            item["university"] = university
            item["location"] = location
            item["department"] = department
            item["programme"] = programme
            item["ucas_code"] = ucas_code
            item["degree_type"] = degree_type
            item["mode"] = mode
            item["overview"] = overview
            item["IELTS"] = IELTS
            item["TOEFL"] = ''
            item["Alevel"] = Alevel
            item["IB"] = IB
            item["teaching_assessment"] = teaching_assessment
            item["career"] = career
            item["tuition_fee"] = tuition_fee
            item["modules"] = modules
            item["duration"] = duration
            item["start_date"] = ''
            item["deadline"] = ''
            item["entry_requirements"] = entry_requirements
            item["url"] = response.url
            item["how_to_apply"] = ''
            item['type'] = 'Taught'
            yield item