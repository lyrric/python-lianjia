# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging

class CommunityPipeline(object):
    config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "lianjia"
    }
    db = pymysql.connect(**config)
    cur = db.cursor()

    def process_item(self, item, spider):
        query_sql = 'select count(*) from community where id = %s'
        self.cur.execute(query_sql, (item['id']))
        row = self.cur.fetchone()
        if row[0] > 0:
            logging.info('数据重复: '+item['id']+','+item['name'])
            return item
        if item['sold_avg_price'] == '暂无':
            item['sold_avg_price'] = 0
        sql = 'insert into  community(id, name,selling_count,sold_avg_price,district,gmt_create) ' \
              'values(%s, %s, %s, %s, %s, now())'

        self.cur.execute(sql,
                         (
                         item['id'], item['name'], item['selling_count'], item['sold_avg_price'], item['district']))
        self.db.commit()

        return item
