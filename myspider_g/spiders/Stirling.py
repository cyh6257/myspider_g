# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider_g.items import HooliItem
from myspider_g.hooli_mode import clear_long_text

class StirlingSpider(CrawlSpider):
    name = 'Stirling'
    allowed_domains = ['www.stir.ac.uk']
    start_urls = ['https://www.stir.ac.uk/s/search.html?collection=stir-courses&f.CourseLevel%7CL=postgraduate+(taught)&f.StudyMethod%7CM=full-time&start_rank=1']
    rules = (
        Rule(LinkExtractor(allow=(r'start_rank=\d+'),restrict_xpaths='//div[@class="columns pagination-centered"]//li'),follow=True),
        Rule(LinkExtractor(restrict_xpaths='//h4/a'),follow=False, callback='parse_item'),
    )
    def parse_item(self, response):
        print('-------------',response.url)
        item=HooliItem()
        #//section[@aria-label="course-header"]/h1/text() 专业名
        programme=response.xpath('//section[@aria-label="course-header"]/h1/text()').extract()
        programme=''.join(programme)
        # print(programme)
        #//section[@aria-label="course-header"]/p/text()
        degree_type=response.xpath('//section[@aria-label="course-header"]/p/text()').extract()
        degree_type=''.join(degree_type).replace('Postgraduate Diploma','').replace('Postgraduate Certificate','').replace(',','').strip()
        # print(degree_type)

        # //section[@aria-label="introduction"]//text()
        overview=response.xpath('//section[@aria-label="introduction"]//text()').extract()
        overview=''.join(overview).strip()
        overview=re.split('\s{2,}',overview)
        overview=''.join(overview)
        keys=response.xpath('//div[@class="key"]//li//text()').extract()

        keys=''.join(keys)
        mode=re.findall('(?i)[a-z]*-time',keys.lower())
        mode=list(set(mode))
        mode=''.join(mode).replace('part-time','')
        start_date=re.findall('Start date:[ \w\(\)\-]*\:?[ \w\(\)]{0,10}',keys)
        start_date=''.join(start_date).replace('Course Director','').replace('Start date:','')

        duration = re.findall('Duration:[\s\w-]*',keys)
        duration = ''.join(duration)
        try:
            entry_requirements1=response.xpath('//section[@aria-label="academic-requirments"]//text()').extract()
        except:
            entry_requirements1=[]
        try:
            entry_requirements2=response.xpath('//section[@aria-label="language-requirements"]//text()').extract()
        except:
            entry_requirements2=[]
        entry_requirements=entry_requirements1+entry_requirements2
        entry_requirements=''.join(entry_requirements)
        entry_requirements2=''.join(entry_requirements2)
        # print(entry_requirements2)
        IELTS=re.findall('IELTS:[\s]*[4-9].\d[ a-zA-Z]*[3-9].\d[ a-zA-Z]*',entry_requirements2)
        IELTS=''.join(IELTS)
        # print(IELTS)
        TOEFL=re.findall('TOEFL:[a-zA-Z\s]*\d{0,3}[\sa-zA-Z]*\d{0,2}',entry_requirements2)
        TOEFL=''.join(TOEFL)
        # print(TOEFL)
        #//*[@id="finance"]//text()
        finace=response.xpath('//*[@id="finance"]//text()').extract()
        finace=''.join(finace)
        try:
            tuition_fee=re.findall('£\d+,\d+',finace)
            tuition_fee='-'.join(tuition_fee).replace(',','').replace('£','')
            tuition_fee=tuition_fee.split('-')
            tuition_fee=list(map(int,tuition_fee))
            tuition_fee=max(tuition_fee)
        except:
            tuition_fee=''
        #//section[@aria-label="course-structure-holder"]//text()
        #//section[@aria-label="course-assessment-holder"]//text()
        try:
            teaching_assessment1=response.xpath('//section[@aria-label="course-assessment-holder"]//text()').extract()
            teaching_assessment2=response.xpath('//section[@aria-label="course-assessment-holder"]//text()').extract()
            teaching_assessment=teaching_assessment1+teaching_assessment2
            teaching_assessment=''.join(teaching_assessment)
        except:
            teaching_assessment=''
        # print(teaching_assessment)


        #//section[@aria-label="modules-holder"]//text()
        modules=response.xpath('//section[@aria-label="modules-holder"]//text()').extract()
        modules=''.join(modules)

        #//section[@aria-label="career-ops"]//text()
        career=response.xpath('//section[@aria-label="career-ops"]//text()').extract()
        career=''.join(career)
        department=response.xpath('//div[@class="photocontact"]/p[2]/text()').extract()
        department=clear_long_text(department).replace('UK','').replace('University of Stirling','').replace('Stirling','').replace('Scotland','').replace('FK9 4LA','').strip()
        department=clear_long_text(department)
        print(department)
        university='University of Stirling'
        item["university"] = university
        item["location"] = ''
        item["department"] = department
        item["programme"] = programme
        item["mode"] = mode
        item["type"] = 'taught'
        item["degree_type"] = degree_type
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = TOEFL
        item["teaching_assessment"] = teaching_assessment
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        item["how_to_apply"] = ''
        item["GPA"]=''
        item["Justone"] = university+programme+degree_type
        item["ucas_code"] = ''
        # yield item