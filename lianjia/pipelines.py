# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
from lianjia import settings
from lianjia.items import SoldHouseItem
from lianjia.spiders.community_spider import CommunitySpider
from lianjia.spiders.selling_house_spider import SellingHouseSpider
from lianjia.spiders.sold_house_spider import SoldHouseSpider


class LianjiaPipeline(object):

    db = pymysql.connect(**settings.DB_CONFIG)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)

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
        logging.info("小区："+item['name'])
        query_sql = 'select count(*) amount from community where id = %s and version = %s'
        self.cur.execute(query_sql, (item['code'], item['version']))
        row = self.cur.fetchone()
        if row['amount'] > 0:
            # 判断是否重复
            logging.info('数据重复: ' + item['code'] + ',' + item['name'])
            return item
        sql = 'insert into  community' \
              '(code, name, selling_house_amount, district, version, gmt_create) ' \
              'values(%s, %s, %s, %s, %s, now())'

        self.cur.execute(sql,
                         (
                             item['code'], item['name'], item['selling_house_amount'], item['district'], item['version']
                         )
                         )
        self.db.commit()

        return item

    # 存储小区信息的售出数量
    def save_community_sold(self, item):
        try:
            logging.info("小区：" + item['name'] + '，售出数量:'+item['sold_house_amount'])
        except Exception as e:
            logging.error(e)
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
        logging.info("售卖中房源code:" + item['code'] + ', ' + item['title'])
        query_sql = 'select count(*) amount from selling_house where code = %s'
        self.cur.execute(query_sql, item['code'])
        row = self.cur.fetchone()
        if row['amount'] == 0:
            sql = 'insert into selling_house(code, community_code, title, price, price_per, ' \
                  'price_unit, type, size, on_sale_date, deleted, ' \
                  'gmt_create, gmt_update) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())'
            self.cur.execute(sql,
                             (
                                 item['code'], item['community_code'], item['title'], item['price'],
                                 item['price_per'], item['price_unit'], item['type'], item['size'],
                                 item['on_sale_date'],  item['deleted']))
        else:
            sql = 'update selling_house set community_code = %s, title = %s, price = %s, price_per = %s, ' \
                  'price_unit = %s, type = %s, size = %s ' \
                  ' on_sale_date = %s, deleted = %s, gmt_update = now() where code = %s '
            self.cur.execute(sql,
                             (
                                 item['community_code'], item['title'], item['price'],
                                 item['price_per'], item['price_unit'], item['type'], item['size'],
                                 item['on_sale_date'], item['deleted'], item['code']))
        self.db.commit()
        return item

    #  存储售出的房源信息
    def save_sold_house(self, item):
        logging.info("售出房源code:" + item['code'] + ', ' + item['title'])
        if item['selling_price'] == '暂无数据':
            item['selling_price'] = None

        query_sql = 'select count(*) amount from sold_house where code = %s'
        self.cur.execute(query_sql, item['code'])
        row = self.cur.fetchone()
        if row['amount'] == 0:
            sql = 'insert into sold_house(code, community_code, title, selling_price, ' \
                  'sold_price, sold_price_per, price_unit, type, size, on_sale_date, sold_date, gmt_create ) ' \
                  'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())'
            self.cur.execute(sql,
                             (
                                 item['code'], item['community_code'], item['title'], item['selling_price'],
                                 item['sold_price'], item['sold_price_per'], item['price_unit'], item['type'],
                                 item['size'], item['on_sale_date'], item['sold_date']))

        self.db.commit()
        return item