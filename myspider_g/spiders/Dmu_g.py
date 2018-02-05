# -*- coding: utf-8 -*-
from myspider_g.items import HooliItem
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
class DmuGSpider(CrawlSpider):
    name = 'Dmu_g'
    allowed_domains = ['www.dmu.ac.uk']
    start_urls = ['http://www.dmu.ac.uk/study/courses/postgraduate-courses/']

    rules = (
        Rule(LinkExtractor(allow=r'postgraduate-courses.aspx\?courselisting1_List_GoToPage=[0-9]{0,2}'),follow=True),
        Rule(LinkExtractor(allow=r'/postgraduate-courses/[a-zA-Z\-]+\/[a-zA-Z\-]+.aspx'), callback='parse_dmu',follow=False),
    )


    def parse_dmu(self, response):
        print('---------------------',response.url)
        item = HooliItem()

        Internationnal = response.xpath('//div[@data-kftab="2"]//text()').extract()
        # print(response.url)
        Course = response.xpath('//div[@class="block__details block__details--overlay block__details--courseOverlay"]//h1[@class="block__details__title"]//text()').extract()[0]
        Course = Course.strip()
        Master = re.findall('[A-Z]{1}[A-Za-z]{1,3}\s?\([a-zA-Z]*\)', Course)
        Master = ''.join(Master)
        programme = Course.replace(Master, '')
        if Master == '':
            Master = re.findall('MA|MSc', Course)
            Master = ''.join(Master)
            # print(Master, Course, response.url)
        else:
            Master = ''
        # 专业描述
        CourseOverview = response.xpath('//div[@class="block large-8 columns course-col2"]//text()').extract()
        overview = ''.join(CourseOverview).strip()
        # 学费
        self.var_fee = 'Fees and funding:'
        self.var_fee_2 = 'Fees and funding 2017/18'
        if self.var_fee in Internationnal:
            index_fee = response.xpath('//div[@data-kftab="2"]//text()').extract().index(self.var_fee)
            tuition_fee = Internationnal[index_fee + 1]
            TuitionFee = re.findall(r"£\d*,?\d*", tuition_fee)

        elif self.var_fee_2 in Internationnal:
            index_fee = response.xpath('//div[@data-kftab="2"]//text()').extract().index(self.var_fee_2)
            tuition_fee = Internationnal[index_fee + 1]
            TuitionFee = re.findall(r"£\d*,?\d*", tuition_fee)
        else:
            TuitionFee = ''
        if TuitionFee != []:
            TuitionFee = ''.join(TuitionFee)
            TuitionFee = re.findall('\d+', TuitionFee)
            tuition_fee = ''.join(TuitionFee)
        else:
            tuition_fee = ''
        # print(TuitionFee,response.url)

        # 地点
        if 'Location:' in Internationnal:
            index_Location = response.xpath('//div[@data-kftab="2"]//text()').extract().index('Location:')
            location = Internationnal[index_Location + 1]
        else:
            location= 'The Gateway Leicester LE1 9BH '


        # 课程长度
        if 'Duration:' in Internationnal:
            index_Tt = response.xpath('//div[@data-kftab="2"]//text()').extract().index('Duration:')
            duration = Internationnal[index_Tt + 1]
        else:
            duration = ''

        # IELTS \d?.\d? .*

        # 申请要求
        standard = response.xpath(
            '//div[@class="row row--block course-section course-section--criteria"]//text()').extract()
        standard = ' '.join(standard)

        IELTS = re.findall('IELTS (.*){0,3} \d+.\d+ .*', standard)
        IELTS = ''.join(IELTS)

        # 课程及评估
        Evaluation_method = response.xpath('//div[@id="cycle-slideshow_course"]//text()').extract()
        Evaluation_method = ' '.join(Evaluation_method)
        teaching_assessment = Evaluation_method.strip()

        # 就业
        Career = response.xpath('//div[@class="row row--block course-section course-section--opps"]//text()').extract()
        career = ''.join(Career).strip()
        # print(Career)

        university = 'De Montfort'
        item["university"] = university
        item["location"] = location
        item["department"] = ''
        item["programme"] = programme
        item["degree_type"] = Master
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["teaching_assessment"] = teaching_assessment
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = teaching_assessment
        item["duration"] = duration
        item["start_date"] = ''
        item["deadline"] = ''
        item["entry_requirements"] = ''
        item["url"] = response.url

        yield item