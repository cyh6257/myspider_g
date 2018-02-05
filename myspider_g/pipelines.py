# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class MyspiderGPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlDB(object):
    def __init__(self):
        try:
            self.conn = pymysql.connect('127.0.0.1','root','123456','hooli',charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print('连接数据库失败：%s'% str(e))

    def close(self):
        self.cursor.close()
        self.conn.close()


class Hooli(MysqlDB):
    def process_item(self, item, spider):
        sql = 'insert into hooli(university,location,department,programme,degree_type,overview,IELTS,TOEFL,teaching_assessment,career,how_to_apply,tuition_fee,modules,duration,start_date,deadline,entry_requirements,url,mode,type,Justone,GPA,ucas_code,portfolio,interview)' \
              'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ' \
              'on duplicate key update department = values (department),type=VALUES (type),modules = values (modules),entry_requirements = values(entry_requirements),location = values(location),programme = values(programme),teaching_assessment = values(teaching_assessment),degree_type = values(degree_type),tuition_fee= values(tuition_fee),duration= VALUES (duration),start_date=VALUES (start_date),IELTS=VALUES (IELTS),TOEFL = values(TOEFL),start_date=VALUES (start_date),ucas_code=VALUES (ucas_code)'
        try:
            self.cursor.execute(sql, (
                item["university"],item["location"],item["department"], item["programme"],  item["degree_type"], item["overview"],
                item["IELTS"],item["TOEFL"], item["teaching_assessment"], item["career"],item["how_to_apply"],
                item["tuition_fee"], item["modules"], item["duration"], item["start_date"], item["deadline"], item["entry_requirements"], item["url"],
                item["mode"], item["type"], item["Justone"], item["GPA"],item["ucas_code"],item["portfolio"],item["interview"]
            ))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(e)
            print("执行sql语句失败")

        return item
