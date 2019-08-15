# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
from lianjia import settings

class LianjiaPipeline(object):
    db = pymysql.connect(**settings.DB_CONFIG)
    cur = db.cursor()

    def process_item(self, item, spider):
        logging.info('title='+item['title'])
        if spider.name == 'community':
            return self.save_community(item)
        else:
            return self.save_house(item)

    # 存储小区信息
    def save_community(self, item):
        query_sql = 'select count(*) from community where id = %s'
        self.cur.execute(query_sql, (item['id']))
        row = self.cur.fetchone()
        if row[0] > 0:
            logging.info('数据重复: ' + item['id'] + ',' + item['name'])
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

    #  存储房源信息
    def save_house(self, item):
        # query_sql = 'select count(*) from house where id = %s'
        # self.cur.execute(query_sql, (item['id']))
        # row = self.cur.fetchone()
        # if row[0] > 0:
        #     logging.info('数据重复: ' + item['id'] + ',' + item['title'])
        #     return item
        sql = 'insert into house(id, community_id, title, price, price_unit, price_per, ' \
              'price_per_unit, type, size, on_sale_date, gmt_create) ' \
              'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())'

        self.cur.execute(sql,
                         (
                             item['id'], item['community_id'], item['title'], item['price'], item['price_unit'],
                             item['price_per'], item['price_per_unit'], item['type'], item['size'], item['on_sale_date']))
        self.db.commit()
        return item
