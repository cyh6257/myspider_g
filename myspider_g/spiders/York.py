# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider_g.items import HooliItem

class YorkSpider(CrawlSpider):
    name = 'York'
    allowed_domains = ['www.york.ac.uk']
    start_urls = ['https://www.york.ac.uk/study/postgraduate/courses/all?mode=taught&q=&level=postgraduate']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@id="results"]/table/tbody/tr/td[@class="coursetitle"]/a'),
             follow=False, callback='parse_item'),
    )

    def parse_item(self, response):
        urls = response.url.split('/')
        if 'masters-courses' in urls:
            print('-------------------------', response.url)

        elif urls[3] == 'study':
            # print('=============================',response.url)
            item = HooliItem()
            university = 'University of York'
            str1 = response.xpath('//div[@id="overview"]//text()').extract()
            # print(str1)
            if 'Department' in str1:
                Department = str1.index('Department')
                department = str1[Department + 1]
            else:
                department = ''
            if 'Length' in str1:
                Duration = str1.index('Length')
                duration= str1[Duration + 1]
            else:
                duration = ''
            if 'Start date' in str1:
                StartDate = str1.index('Start date')
                StartDate = str1[StartDate + 1]
                start_date = StartDate.replace('(', '')
            else:
                start_date= ''

            CourseOverview = response.xpath(
                '//div[@class="o-grid__box o-grid__box--half o-grid__box--half@medium"]//text()').extract()
            overview = ''.join(CourseOverview)

            # //div[@class="o-grid__box o-grid__box--twothirds o-grid__box--full@medium"]
            Modules = response.xpath(
                '//div[@class="o-grid__box o-grid__box--twothirds o-grid__box--full@medium"]//text()').extract()
            modules = ''.join(Modules)

            Fees = response.xpath('//div[@class="o-grid__box o-grid__box--twothirds"]//text()').extract()
            Fees = ''.join(Fees)
            TuitionFee = re.findall('Full-time\s*.*\s*£\d{2},\d{3}', Fees)
            TuitionFee = re.findall('£\d{2},\d{3}', ''.join(TuitionFee))
            TuitionFee = ''.join(TuitionFee)
            TuitionFee = TuitionFee.replace(',', '')
            tuition_fee = TuitionFee.replace('£', '')
            Assessment = response.xpath(
                '//div[@class="o-grid__box o-grid__box--half o-grid__box--half@medium o-grid__box--full@small"]//text()').extract()
            teaching_assessment = ''.join(Assessment)
            # print(Assessment)
            EntryRequirement = response.xpath('//div[@id="entry"]//text()').extract()
            # \d+\.\d?[\sa-zA-Z]*\d+.\d?.*
            IELTS = re.findall('\d+\.\d?[\sa-zA-Z]*\d+.\d?.*', ''.join(EntryRequirement))
            IELTS = ''.join(IELTS)
            TOEFL = re.findall('TOEFL[\s:.]*\d+,[a-zA-Z0-9, ]*', ''.join(EntryRequirement))
            TOEFL = ''.join(TOEFL)
            entry_requirements = ''.join(EntryRequirement)

            Career = response.xpath('//div[@class="o-grid__box o-grid__box--half"]//text()').extract()
            career = ''.join(Career)

            Course = response.url.split('/')[-2]
            Master = Course.split('-')[0]
            Course = ' '.join(Course.split('-'))
            programme= Course.replace(Master, '').strip().capitalize()
            degree_type= Master.upper()
            university='University of York'
            item["university"] = university
            item["location"] = ''
            item["department"] = department
            item["programme"] = programme
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
            # print(item)
            yield item