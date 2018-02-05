# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderGItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# class HooliItem(scrapy.Item):
#     University = scrapy.Field()
#     Department = scrapy.Field()
#     Programme = scrapy.Field()
#     Overview = scrapy.Field()
#     CourseCode = scrapy.Field()
#     StartDate = scrapy.Field()
#     Duration = scrapy.Field()
#     Modules = scrapy.Field()
#     Assessment = scrapy.Field()
#     Career = scrapy.Field()
#     ApplicationDate = scrapy.Field()
#     Deadline = scrapy.Field()
#     EntryRequirements = scrapy.Field()
#     TuitionFee = scrapy.Field()
#     IELTS = scrapy.Field()
#     TOEFL = scrapy.Field()
#     Alevel = scrapy.Field()
#     IB = scrapy.Field()
#     url = scrapy.Field()
#     Location = scrapy.Field()
#     other = scrapy.Field()
#     Master = scrapy.Field()
class HooliItem(scrapy.Item):
    university = scrapy.Field()
    department = scrapy.Field()
    programme = scrapy.Field()
    degree_type = scrapy.Field()
    overview = scrapy.Field()
    ucas_code= scrapy.Field()
    start_date = scrapy.Field()
    mode = scrapy.Field()
    type = scrapy.Field()
    duration = scrapy.Field()
    modules = scrapy.Field()
    teaching_assessment = scrapy.Field()
    career = scrapy.Field()
    application_date = scrapy.Field()
    deadline = scrapy.Field()
    application_fee = scrapy.Field()
    entry_requirements = scrapy.Field()
    tuition_fee = scrapy.Field()
    IELTS = scrapy.Field()
    TOEFL = scrapy.Field()
    Alevel = scrapy.Field()
    IB = scrapy.Field()
    url = scrapy.Field()
    location = scrapy.Field()
    other = scrapy.Field()
    how_to_apply = scrapy.Field()
    description_degree = scrapy.Field()
    Justone = scrapy.Field()
    GPA = scrapy.Field()
    interview = scrapy.Field()
    portfolio= scrapy.Field()
