# -*- coding: utf-8 -*-

import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from random import uniform

import pymysql
from pydispatch import dispatcher
from scrapy import signals

from lianjia import settings
from lianjia.items import SoldHouseItem, CommunityItem, SellingHouseItem
from lianjia.spiders.community_spider import CommunitySpider
from lianjia.spiders.selling_house_spider import SellingHouseSpider
from lianjia.spiders.sold_house_spider import SoldHouseSpider


class LianjiaPipeline(object):

    db = None
    cur = None

    amount = 0  # 已保存数据

    def __init__(self) -> None:
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.db = pymysql.connect(**settings.DB_CONFIG)
        self.cur = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    list = []

    # 爬虫执行完成后执行保存动作
    def spider_closed(self, spider):
        logging.info('数据采集完毕---------------------------------------------------执行保存操作')
        item = None
        if spider.name == CommunitySpider.name:
            # 完成之后让version + 1
            self.cur.execute('update version set version = (version + 1) ')
            self.db.commit()
            item = CommunityItem()
        elif spider.name == SellingHouseSpider.name:
            item = SellingHouseItem()
        elif spider.name == SoldHouseSpider.name:
            item = SoldHouseItem()
        item['finish'] = True
        self.process_item(item, spider)
        self.db.close()
        self.cur.close()

    def process_item(self, item, spider):
        if spider.name == CommunitySpider.name:
            return self.save_community(item)
        elif spider.name == SellingHouseSpider.name:
            return self.save_selling_house(item)
        elif spider.name == SoldHouseSpider.name:
            if isinstance(item, SoldHouseItem):
                self.save_sold_house(item)
            else:
                self.save_community_sold(item)

    # 存储小区信息
    def save_community(self, item):
        if not item['finish']:
            #logging.debug("小区："+item['name'])
            query_sql = 'select count(*) amount from community where id = %s and version = %s'
            self.cur.execute(query_sql, (item['code'], item['version']))
            row = self.cur.fetchone()
            if row['amount'] > 0:
                # 判断是否重复
                logging.info('数据重复: ' + item['code'] + ',' + item['name'])
                return item
            self.list.append(item)
            self.amount += 1
        if len(self.list) == 30 or (item['finish'] and len(self.list) != 0):
            i = 0
            sql = 'insert into  community' \
                  '(code, name, selling_house_amount, district, version, gmt_create) ' \
                  'values'
            while i < len(self.list):
                sql += '("{}", "{}", {}, "{}", {}, now())'
                if i != (len(self.list)-1):
                    sql += ','
                sql = sql.format(self.list[i]['code'],  self.list[i]['name'], self.list[i]['selling_house_amount'], self.list[i]['district'], self.list[i]['version'])
                i += 1
            self.cur.execute(sql)
            self.db.commit()
            self.list.clear()
            logging.info("已保存数据:" + str(self.amount))
            return item

    # 存储小区信息的售出数量
    def save_community_sold(self, item):
        sql = 'update community set sold_house_amount = %s where code = %s and version = %s'
        self.cur.execute(sql,
                         (
                             item['sold_house_amount'], item['code'], item['version']
                         )
                         )
        self.db.commit()
        return item

    #  存储售卖中的房源信息
    def save_selling_house(self, item):
        if not item['finish']:
            #logging.debug("售卖中房源code:" + item['code'] + ', ' + item['title'])
            query_sql = 'select count(*) amount from selling_house where code = %s'
            self.cur.execute(query_sql, item['code'])
            row = self.cur.fetchone()
            if row['amount'] == 0:
                self.list.append(item)
                self.amount += 1
            else:
                sql = 'update selling_house set community_code = %s, title = %s, price = %s, price_per = %s, ' \
                      'price_unit = %s, type = %s, size = %s ,' \
                      ' on_sale_date = %s, deleted = %s, gmt_update = now() where code = %s '
                self.cur.execute(sql,
                                 (
                                     item['community_code'], item['title'], item['price'],
                                     item['price_per'], item['price_unit'], item['type'], item['size'],
                                     item['on_sale_date'], item['deleted'], item['code']))
                self.db.commit()

        if len(self.list) == 30 or (item['finish'] and len(self.list) != 0):
            try:
                i = 0
                sql = 'insert into selling_house(code, community_code, title, price, price_per, ' \
                      'price_unit, type, size, on_sale_date, deleted, ' \
                      'gmt_create, gmt_update) values'
                while i < len(self.list):
                    sql += '("{}", "{}", "{}", {}, {}, "{}", "{}", "{}", "{}", {}, now(), now())'
                    if i != (len(self.list) - 1):
                        sql += ','
                    sql = sql.format(
                        self.list[i]['code'], self.list[i]['community_code'], self.list[i]['title'], self.list[i]['price'],
                        self.list[i]['price_per'], self.list[i]['price_unit'], self.list[i]['type'], self.list[i]['size'],
                        self.list[i]['on_sale_date'], self.list[i]['deleted']
                    )
                    i += 1
                self.cur.execute(sql)
                self.db.commit()
                self.list.clear()
                logging.info("已保存数据:" + str(self.amount))
            except Exception as e:
                logging.error(e)
                raise e
        return item

    #  存储售出的房源信息
    def save_sold_house(self, item):
        if not item['finish']:
            #logging.debug("售出房源code:" + item['code'] + ', ' + item['title'])
            query_sql = 'select count(*) amount from sold_house where code = %s'
            self.cur.execute(query_sql, item['code'])
            row = self.cur.fetchone()
            if row['amount'] == 0:
                self.list.append(item)
                self.amount += 1
        if len(self.list) == 30 or (item['finish'] and len(self.list) != 0):
            sql = 'insert into sold_house(code, community_code, title, selling_price, ' \
                  'sold_price, sold_price_per, price_unit, type, size, on_sale_date, sold_date, gmt_create ) ' \
                  'values'
            i = 0
            while i < len(self.list):
                sql += '("{}", "{}", "{}", {}, {}, "{}", "{}", "{}", "{}", {}, "{}", now())'
                if i != (len(self.list)-1):
                    sql += ','
                sql = sql.format(self.list[i]['code'], self.list[i]['community_code'], self.list[i]['title'], self.list[i]['selling_price'],
                                 self.list[i]['sold_price'], self.list[i]['sold_price_per'], self.list[i]['price_unit'], self.list[i]['type'],
                                 self.list[i]['size'], self.list[i]['on_sale_date'], self.list[i]['sold_date'])
                i += 1
            self.cur.execute(sql)
            self.db.commit()
            self.list.clear()
            logging.info("已保存数据:"+str(self.amount))
        return item