# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider_g.items import HooliItem

class BrunelSpider(CrawlSpider):
    name = 'Brunel'
    allowed_domains = ['www.brunel.ac.uk']
    start_urls = ['http://www.brunel.ac.uk/study/Course-listing?courseLevel=0%2f2%2f24%2f28%2f44&page=0&studyMode=full-time']
    rules = (
        Rule(LinkExtractor(allow=r'www.brunel.ac.uk/study/Course-listing\?courseLevel=0%2f2%2f24%2f28%2f44&page=[0-9]+&studyMode=full-time$'),follow=True),
        Rule(LinkExtractor(allow=r'www.brunel.ac.uk/study/postgraduate/.*'), follow=False, callback='parse_item'),
    )
    def parse_item(self, response):
        print('-------------',response.url)
        # print('11111111111111111')
        item = HooliItem()
        longstr = response.xpath('//div[@class="featureBlock clearfix"]//text()').extract()
        # print(longstr,response.url)
        if 'Mode of study' in longstr:
            index_Duration = longstr.index('Mode of study')
            Duration = longstr[index_Duration + 2]
            duration = ''.join(Duration).strip()
            # print(Duration,response.url)
        else:
            duration= ''
        if 'Start date' in longstr:
            index_Duration = longstr.index('Start date')
            StartDate = longstr[index_Duration + 2]
            start_date= ''.join(StartDate).strip()
            # print(StartDate,response.url)
        else:
            start_date= ''

        # 专业名
        try:
            Course = response.url.split('/')[-1]
            degree_type = Course.split('-')[-1]
            Course = ' '.join(Course.split('-'))
            programme = Course.replace(degree_type, '')
            # print(Course,Master,response.url)
        except:
            programme = ''

        # 雅思
        IELTS = response.xpath('//div[@class="featureBlock"]//li//text()').extract()[0]
        IELTS = IELTS.replace('IELTS:', '')
        # print(IELTS,response.url)

        # 学费
        try:
            TuitionFee = response.xpath('//div[@class="featureBlock"]/p/span/text()').extract()
            index_TuitionFee = TuitionFee.index('International students:')
            TuitionFee = TuitionFee[index_TuitionFee + 1]
            TuitionFee = TuitionFee.replace(',', '')
            tuition_fee = TuitionFee.replace('£', '')
            # print(TuitionFee,response.url)
        except:
            tuition_fee = ''
            print(response.url, '------------------------------------------')

        # //h4[@id="assessment"]/following-sibling::*
        # 评估
        Assessment = response.xpath('//h4[@id="assessment"]/following-sibling::*//text()').extract()
        teaching_assessment = ''.join(Assessment).strip()
        # print(Assessment,response.url)

        # //h2[@id="entrycriteria"]/following-sibling::ul
        # 入学要求
        EntryRequirements = response.xpath('//h2[@id="entrycriteria"]/following-sibling::ul//text()').extract()
        entry_requirements = ''.join(EntryRequirements).strip()
        # print(EntryRequirements,response.url)

        # 课程设置
        Modules = response.xpath('//h2[@id="coursecontent"]/following-sibling::*//text()').extract()
        clear_str = Modules.index('Back to top')
        Modules = Modules[0:clear_str]
        modules = ''.join(Modules)
        # print(Modules,response.url)

        # 专业描述
        # //h2[@id="overview"]/following-sibling::*//text()
        CourseOverview = response.xpath('//h2[@id="overview"]/following-sibling::*//text()').extract()
        clear_str_2 = CourseOverview.index('Back to top')
        CourseOverview = CourseOverview[0:clear_str_2]
        overview = ''.join(CourseOverview)

        item["university"] = 'Brunel University London'
        item["location"] = ''
        item["department"] = ''
        item["programme"] = programme
        item["degree_type"] = degree_type
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["teaching_assessment"] = teaching_assessment
        item["career"] = ''
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url

        yield item