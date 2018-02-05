# -*- coding: utf-8 -*-
from myspider_g.items import HooliItem
import re
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from myspider_g.hooli_mode import find_fee_s

class StandrewsSpider(CrawlSpider):
    name = 'StAndrews'
    allowed_domains = ['www.st-andrews.ac.uk']
    start_urls = ['https://www.st-andrews.ac.uk/subjects/']

    rules = (
        Rule(LinkExtractor(allow=(r'.*'), restrict_xpaths=('//div[@class="container"]//h4')), follow=True),
        Rule(LinkExtractor(allow=(r''), restrict_xpaths=('//div[@class="col-sm-6 content"]/table')), follow=False,callback='parse_item'),
    )

    def parse_item(self, response):
        print('--------',response.url)

        item = HooliItem()
        programme = response.xpath('//section//h2//text()').extract()[0]

        long_str = response.xpath('//section[@class="sta-grey-light course"]//text()').extract()
        # print(long_str, response.url)

        Master = response.url.split('/')
        Master = Master[-2]
        Master = Master.split('-')
        degree_type = Master[-1].upper()




        long_str_date = ''.join(long_str)
        StartDate = re.findall('Start.+', long_str_date)
        if StartDate:
            start_date = StartDate[0]
        else:
            start_date = ''

        Deadline = re.findall('End.+', long_str_date)
        if Deadline:
            deadline= Deadline[0]
            # print(Deadline)
        else:
            deadline = ''

        # IELTS
        allp=response.xpath('//p/text()').extract()
        allp=''.join(allp)
        IELTS=re.findall('IELTS[\:\sa-zA-Z]*\d.\d[a-zA-Z\s\,]*\d.\d[\s\,\(a-zA-Z]*',allp)
        IELTS=''.join(IELTS)
        # print(IELTS)
        findtime=response.xpath('//div[@class="row"]//p//text()').extract()
        findtime=''.join(findtime)
        # print(findtime)
        duration = re.findall('[a-zA-Z\s]{0,8}year[s]?\sfull\stime',findtime)
        duration=''.join(duration)
        mode=re.findall('full\stime',findtime)
        mode=''.join(mode)
        ucas_code=re.findall('[A-Z]\d{3}',findtime)
        ucas_code=''.join(ucas_code).replace('C013','')

#         if ucas_code=='':
#             how_to_apply=['Taught programmes',
# 'Before applying to study for a taught programme at the University, ensure that you can meet all of the University’s minimum entrance requirements. The information below includes details on how and when to apply for our taught programmes.',
# 'Admission to a taught programme is normally on the basis of a good first degree with Honours from a UK university (or its overseas equivalent). Final overall grade examples include 2.1 (UK), 2.2 or B+ (Europe), 3.6 GPA (USA), 85% (China), 70% (India). More details can be found in entry requirements and country information.',
# 'We do not require the GMAT.',
# 'English language requirements',
# 'Applicants whose first language is not English must provide evidence of English proficiency. For further information on what evidence of English proficiency is required please email: international@st-andrews.ac.uk',
# 'Applicants to the MSc Marine Mammal Science, the MSc in Astrophysics, or any postgraduate taught courses in the Department of Film Studies or the School of English must also complete a supplementary application form',
# 'All applications are made using our online form and the following supplementary documentation must be uploaded in the section provided before a decision can be made:',
# 'CV or résumé. This should include your personal details with a history of your education and employment to date.',
# 'A sample of academic written work in English - see further guidance below.',
# 'Two original signed academic references.',
# 'Academic transcripts and degree certificates. Please only upload certified copies with official English translations if applicable. Do not send original documents as they cannot be returned.',
# 'English language requirements certificate.',
# 'Covering letter (optional).',
# 'Written work sample and personal statements',
# 'Applicants who cannot provide a sample of work or personal statement as listed below should contact the appropriate School directly for further guidance.',
# 'The sample of written work can be an extract from a previous project or essay, or part of your undergraduate dissertation.',
# 'All written work and personal statements must be provided in English.',
# 'Faculty of Arts and Faculty of Divinity',
# 'All applications submitted to the Faculty of Arts and the Faculty of Divinity should include a 2,000 word sample of written work unless stated otherwise.',
# 'Faculty of Science',
# 'Students applying for programmes run by Schools within the Faculty of Science are not expected to submit a sample of their written work, with the exception of applicants to the Sustainable Development MSc.',
# 'School of Art History',
# 'All applications to programmes offered by the School of Art History should include a brief personal statement of approximately 500 words along with the academic written sample.',
# 'School of Classics',
# 'All applications submitted to the School of Classics should provide a sample of written work between 2,500 and 5,000 words in length and a letter of intent. The letter of intent should include why you wish to study for an MLitt in Classics at St Andrews; your suitability for the programme; the areas that you are keen to specialise in; possible areas for dissertation study; any future plans for further research or careers beyond the MLitt. The School of Classics does not expect clearly worked-out proposals, or even that you have identified a single area for your research project, just an indication of your particular areas of interest.',
# 'School of International Relations',
# 'All applications submitted to the School of International Relations should include a brief personal statement of approximately 500 words stating why you wish to study at the University of St Andrews and your reasons for selecting the programme.',
# 'School of Management',
# 'All applications submitted to the School of Management should include a brief personal statement of approximately 500 words instead of the academic written sample.',
# 'Department of Philosophy',
# 'All applications submitted to the Department of Philosophy should provide a sample of written work of no more than 2,500 words in length.',
# 'The Graduate School',
# 'Students applying for programmes run by the Graduate School are not expected to submit a sample of their written work.',
# 'References',
# 'Two academic references. References are normally requested by email directly to your referees when you submit your application form. Applicants remain responsible for ensuring that references are sent to us.',
# 'If preferred, references may be sent by post or email. By email, they must be sent directly from your referees’ own email addresses. By post, they must be sent either directly from your referees, or forwarded by you in a sealed envelope. Referees may use their own headed paper, and they must include your full name and proposed programme of study in their reference.',
# 'One employment reference and one academic reference is acceptable for applicants unable to provide two academic references.',
# 'If you are applying to more than one programme, references will be required for each programme.',
# 'If you are applying to more than one programme, please ensure that each application contains a copy of your supporting documents, as this will allow your application to be processed faster.',
# 'The online application form can be saved and returned to at any point before submitting.',
# 'The majority of taught Masters programmes will start in September of each year with the exception of some distance learning programmes.',
# 'Most programmes do not have a closing date, though an early application would be advisable. This is to allow sufficient time to process our decision and, importantly, to give you time to obtain visas, apply for scholarships and organise travel arrangements, if needed.',
# 'The following programmes have specific application deadline dates:',
# 'Bible and the Contemporary World (distance learning and residential) - 13 June 2018 for September 2018 entry; 1 November 2018 for January 2019 entry (DL only).',
# 'School of English (all Master programmes) - 31 May 2018 to be eligible for scholarships. All other applications up to the 1 June 2018.',
# 'Computer Science Master programmes (with English language option) - 1 November 2017 for January 2018 entry.',
# 'MSc Evolutionary and Comparative Psychology: The Origins of Mind - 31 May 2018.',
# 'School of International Relations (all Master programmes): 30 April 2018.',
# 'MSc Marine Mammal Science: 30 March 2018.',
# 'MLitt Museum and Gallery Studies - 31 May 2018.',
# 'School of Philosophy (all Master programmes) - 1 August 2018.',
# 'MSc Psychology (Conversion): 9 February 2018.',
# 'MLitt Terrorism and Political Violence (Residential and Distance Learning): 30 April 2018.',
# 'Decisions normally take around four to six weeks once all supporting documents and references have been received and the application is complete with the exception of the MSc Psychology (Conversion) and MSc Marine Mammal Science when decisions will be sent out after the closing date.',
# 'Tuition fees will vary depending on what programme you are studying and where you are from. You may be able to apply for help with funding your studies at the University.',
# 'Early application is strongly advised if you are applying for a scholarship. Many have an early closing date (often between December and February) and most scholarships require you to be holding an offer in order to be considered for funding.',
# 'We continue to accept self-funded applications even after scholarship deadlines have passed. If you need further guidance on this, please contact the School that you are applying to.',
# 'For more advice on scholarships and funding, please go to postgraduate scholarships. You can also find out more about our current tuition fees.',
# 'Applicants can disclose the details of any disabilities or specific learning needs that they have in the relevant section of the application form. This information will be passed on to the disability team within Student Services. Applicants are encouraged to get in touch with the disability team (email theasc@st-andrews.ac.uk) as early as possible to ensure that their needs will be met by the University.',
# 'If you are a student with a disability or specific learning need, and the University has not been made fully aware of your requirements prior to an offer being made, we cannot guarantee that suitable resources will be available on your arrival in St Andrews.',
# 'Please note that all applications are assessed purely on academic merit and the impact of a disability will be considered only after a final decision has been made.',]
#             how_to_apply=''.join(how_to_apply)
#             GPA=['Postgraduate candidates will be expected to hold a Bachelor s degree from a prestigious university with an overall mark of 85% or above,The degree of MD (Medicine) requires a medical qualification that is recognised by the UK General CouncilPostgraduate entrance requirements may be higher depending on the School and the programme you wish to study. For more information please contact the international team in Admissions by emailing pgrecruitment@st-andrews.ac.uk This information is for general guidance; we consider each application on its own merits, as outlined in the admissions policy.']
#             GPA=''.join(GPA)
#         else:
#             how_to_apply=''
#             GPA=''

        # print(ucas_code)
        # print(duration)
        # CourseOverview
        CourseOverview = response.xpath('//div[@class="container course"]/div/div/p//text()|//div[@class="container course"]/div/div/ul/li//text()').extract()
        overview = ''.join(CourseOverview)
        # Assessment
        Assessment = response.xpath('//section[3]//text()').extract()
        teaching_assessment = ''.join(Assessment).strip()
        # Modules
        Modules = response.xpath('//div[@id="year-tabs"]//text()').extract()
        modules = ''.join(Modules).strip()
        # TuitionFee
        Fee = response.xpath('//div[@class="container"]//text()').extract()
        tuition_fee=find_fee_s(Fee)
        # print(tuition_fee)


        # Career
        Career = response.xpath('//section[6]//text()').extract()
        career = ''.join(Career).strip()
        department=response.xpath('//section[@class="course sta-grey-light"]//p/strong/text()|//div[@class="container course"]/div/div/strong/text()|//section[@class="course "]/div[@class="container"]/div[@class="row"]/div[@class="col-sm-6 content"]//strong/text()').extract()
        department=''.join(department)
        # print(department)
        entry_requirements = ''.join(long_str).strip()
        university='StAndrews'
        Justone=university+programme+degree_type
        Justone=''.join(Justone)
        # print(Justone)
        item["university"] = university
        item["location"] = 'N/A'
        item["department"] = department
        item["programme"] = programme
        item["ucas_code"] = ucas_code
        item["degree_type"] = degree_type
        item["overview"] = overview
        item["IELTS"] = IELTS
        item["TOEFL"] = ''
        item["teaching_assessment"] = teaching_assessment
        item["career"] = career
        item["tuition_fee"] = tuition_fee
        item["modules"] = modules
        item["duration"] = duration
        item["start_date"] = start_date
        item["deadline"] = deadline
        item["entry_requirements"] = entry_requirements
        item["url"] = response.url
        item["how_to_apply"]=''
        item["mode"] = mode
        item["Justone"] = Justone
        item["GPA"] = ''
        item["type"] = ''
        yield item