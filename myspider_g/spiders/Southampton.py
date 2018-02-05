# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
import re
from myspider_g.items import HooliItem

class SouthamptonSpider(CrawlSpider):
    name = 'Southampton'
    allowed_domains = ['www.southampton.ac.uk']
    start_urls = ['https://www.southampton.ac.uk/courses/taught-postgraduate.page']
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="uos-all-course-groups"]/dl/dd/a'), follow=False,callback='parse_item'),
    )


    def parse_item(self, response):

        print('-------------------------------------------', response.url)
        item = HooliItem()
        # 专业
        Course = response.xpath('//h1[@class="uos-page-title uos-main-title"]//text()').extract()
        Course = ''.join(Course)
        # print(Course)
        # 学位类型
        degree_type = response.xpath('//aside/dl/dd/text()').extract()[0]

        Course = Course.replace(degree_type, '')
        programme = Course.strip()

        # 专业描述
        # //div[@class="uos-page-intro"]//text() 专业描述第一部分
        # //div[@class="uos-grid uos-grid-2-3"]//text() 第二
        part1 = response.xpath('//div[@class="uos-page-intro"]//text() ').extract()
        part2 = response.xpath('//div[@class="uos-grid uos-grid-2-3"]//text()').extract()
        part3 = response.xpath('//div[@data-target="tabset-1"]//text()').extract()
        CourseOverview = part1 + part2 + part3
        overview = ''.join(CourseOverview).strip()

        # 学术要求
        xsyq = response.xpath('//div[@data-target="tabset-2"]//text()').extract()
        # print(xsyq,response.url)

        # 用来区分有无评估标签
        len_div = response.xpath('//div[@id="js-component-tabs"]/h3/text()').extract()
        len_div = len(len_div)
        # 评估
        if len_div >= 6:
            Assessment = response.xpath('//div[@data-target="tabset-6"]//text()').extract()
            teaching_assessment = ''.join(Assessment)
        else:
            teaching_assessment = 'uncleared'

        # 课程要求
        Modules = response.xpath('//div[@data-target="tabset-3"]//text()').extract()
        modules = ''.join(Modules)
        # print(Modules)

        # 就业
        Career = response.xpath('//div[@data-target="tabset-5"]//text()').extract()
        career = ''.join(Career)

        # 学费
        TuitionFee = response.xpath('//table[@class="uos-table"]//text()').extract()
        if TuitionFee != []:
            if 'Full-time' in TuitionFee:
                index_fee = TuitionFee.index('Full-time') + 2
                TuitionFee = TuitionFee[index_fee]
                tuition_fee = TuitionFee.replace(',', '').replace('£', '')
            else:
                tuition_fee= ''
        else:
            tuition_fee = ''
        EntryRequirements = response.xpath('//div[@data-target="tabset-2"]//text()').extract()
        entry_requirements = ''.join(EntryRequirements)

        university = 'Southampton'
        # other=''.join(xsyq).strip()
        Duration = re.findall('\(\d.*\)', Course)
        duration = ''.join(Duration)

        item["university"] = university
        item["location"] = ''
        item["department"] = ''
        item["programme"] = programme
        item["degree_type"] = degree_type
        item["overview"] = overview
        item["IELTS"] = ''
        item["TOEFL"] = ''
        item["teaching_assessment"] = teaching_assessment
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] =''
        item["deadline"] = ''
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        yield item