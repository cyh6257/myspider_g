# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider_g.items import HooliItem
from myspider_g.hooli_mode import clear_long_text,find_fee_s,find_title

class ArtsSpider(CrawlSpider):
    name = 'Arts'
    allowed_domains = ['arts.ac.uk']
    start_urls = ['http://search.arts.ac.uk/s/search.html?collection=courses&query=&profile=_default&f.Course+level%7Cl=Postgraduate&f.Mode%7Cm=Full+time&start_rank=1']
    rules = (
        Rule(LinkExtractor(allow=r'start_rank=[0-9]+'),follow=True),
        # Rule(LinkExtractor(allow=r'arts.ac.uk/[a-z-]+/'), follow=False, callback='parse_arts_g'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="search-title"]//h2'), follow=False, callback='parse_arts_g'),
    )
    error_list = []
    def parse_arts_g(self, response):
        a=response.url
        a=a.split('/')
        print('--------------------------',response.url)
        item = HooliItem()
        #学校 University of the Arts London
        #学院
        try:
            department=response.xpath('//nav[@class="college"]//text()').extract()[0]
        except:
            department=''
        # #学位类型
        Master=response.url.split('/')
        Master=Master[-2]
        degree_type=Master.split('-')[0].upper()
        # print(Master)
        Course =response.xpath('//h1/text()').extract()[0]
        programme=Course.replace(degree_type,'').strip()
        # print(Course)


        url_long_str=response.xpath('//div[@class="ual-container"]//text()').extract()

        # 入学时间
        str_startdate='Start date'
        index_startdate=url_long_str.index(str_startdate)
        start_date=url_long_str[index_startdate+1]

        #课程长度
        str_Duration='Course length'
        index_Duration=url_long_str.index(str_Duration)
        duration=url_long_str[index_Duration+1]

        #课程描述
        #//div[@id="tab1-panel"]//text()
        CourseOverview=response.xpath('//div[@id="tab1-panel"]//text()').extract()
        overview=''.join(CourseOverview)

        #课程设置
        Modules=response.xpath('//div[@id="tab2-panel"]//text()').extract()
        modules=''.join(Modules)

        #申请要求

        how_to_apply=response.xpath('//div[@id="tab3-panel"]//text()').extract()
        deadline = find_title('When to apply',how_to_apply)
        if deadline=='':
            deadline=find_title('Application deadline',how_to_apply)
        elif deadline=='':
            deadline=find_title('START YOUR APPLICATION NOW',how_to_apply)
        else:
            deadline=''
        deadline=''.join(deadline)
        interview=find_title('Interview criteria',how_to_apply)
        if interview=='':
            interview=find_title('INTERVIEW ADVICE',how_to_apply)
        elif interview=='':
            interview=find_title('Interview',how_to_apply)
        interview=''.join(interview)
        entry_requirements = find_title('Entry Requirements', how_to_apply)
        if entry_requirements=='':
            entry_requirements=find_title('Entry requirements',how_to_apply)
        entry_requirements=''.join(entry_requirements)
        how_to_apply=''.join(how_to_apply)
        IELTS = re.findall('IELTS[\sa-zA-Z]*\d.\d[ \w\(\),\.]*', how_to_apply)
        IELTS=''.join(IELTS)

        url_long_str2=response.xpath('//div[@id="tab4-panel"]//text()').extract()
        url_long_str2=''.join(url_long_str2)
        # 学费
        tuition_fee = find_fee_s(url_long_str2)
        # print(tuition_fee, '----------------', IELTS)


        # print(url_long_str2)
        #就业方向
        Career=response.xpath('//div[@id="tab5-panel"]//text()').extract()
        career=''.join(Career)

        Location=response.xpath('//div[@itemprop="address"]//text()').extract()
        Location=''.join(Location).strip()
        # print(Location)


        university='University of the Arts London'
        item["university"] = university
        item["location"] = Location
        item["department"] = department
        item["programme"] = programme
        item["degree_type"] = degree_type
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["teaching_assessment"] = ''
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = deadline
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        item["how_to_apply"] = how_to_apply
        item["type"] = 'Taught'
        item["mode"] = 'full-time'
        item["interview"] = interview
        item["portfolio"] = 'http://www.arts.ac.uk/study-at-ual/apply/portfolio-preparation/'
        item["Justone"] = response.url
        item["GPA"] = ''
        item["ucas_code"] = ''
        yield item
