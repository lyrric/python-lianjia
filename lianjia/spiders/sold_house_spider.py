import scrapy
import pymysql
from lianjia import settings
import json
import logging
from lianjia.items import SellingHouseItem, SoldHouseItem
from lianjia.items import CommunityItem
"""爬取房屋信息
"""
class SoldHouseSpider(scrapy.Spider):

    name = 'sold_house'

    base_url = 'https://cd.lianjia.com/chengjiao/'
    db = pymysql.connect(**settings.DB_CONFIG)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)

    def start_requests(self):
        sql = '''
        select * from community where sold_house_amount is null
        '''
        # sql = 'select * from community where selling_house_amount ' \
        #       '<> 0 and version = (select version from version limit 1)'
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            yield scrapy.Request(url=self.base_url + 'c' + row['code'], meta=row, callback=self.parse_index)

    # 解析列表首页，获取列表页数
    def parse_index(self, response):
        item = CommunityItem()
        sold_house_amount = response.xpath('//div[@class="total fl"]/span/text()').extract()[0]
        item['sold_house_amount'] = sold_house_amount
        item['code'] = response.meta['code']
        item['name'] = response.meta['name']
        item['version'] = response.meta['version']
        yield item

        community_code = response.meta['code']
        community_name = response.meta['name']

        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()

        if page_data is None or len(page_data) == 0:
            total_page = 1
        else:
            page_data = page_data[0]
            dict_page_data = json.loads(page_data)
            total_page = dict_page_data['totalPage']
        page = 1
        while page <= total_page:
            logging.info('正在解析小区:' + community_name + ',第' + str(page) + '页，共' + str(total_page) + '页')
            yield scrapy.Request(url=self.base_url + '/pg' + str(page) + 'c' + community_code,
                                 callback=self.parse_house_list)
            page = page + 1

    # 解析房源列表
    def parse_house_list(self, response):
        house_urls = response.xpath('//div[@class="title"]/a/@href').extract()
        deal_dates = response.xpath('//div[@class="dealDate"]/text()').extract()
        i = 0
        while i < len(house_urls):
            yield scrapy.Request(house_urls[i], meta={'deal_date': deal_dates[i]}, callback=self.parse_house_detail)
            i += 1

    # 解析房源详情
    def parse_house_detail(self, response):
        item = SoldHouseItem()
        item['code'] = response.xpath(
            '//div[@class="house-title LOGVIEWDATA LOGVIEW"]/@data-lj_action_resblock_id').extract()[0]  # 房源code
        item['community_code'] = response.xpath(
            '//div[@class="house-title LOGVIEWDATA LOGVIEW"]/@data-lj_action_housedel_id').extract()[0]  # 小区code
        item['title'] = response.xpath('//div[@class="wrapper"]/text()').extract()[0]  # 标题
        item['selling_price'] = response.xpath('//div[@class="msg"]/span/label/text()').extract()[0]  # 挂牌价格
        item['sold_price'] = response.xpath('//span[@class="dealTotalPrice"]/i/text()').extract()[0]  # 售出价格
        item['price_unit'] = response.xpath('//span[@class="dealTotalPrice"]/text()').extract()[0]  # 价格单位（万）
        item['type'] = response.xpath('//div[@class="content"]/ul/li/text()').extract()[0]  # 两室一厅
        item['size'] = response.xpath('//div[@class="content"]/ul/li/text()').extract()[4]  # 大小
        item['on_sale_date'] = response.xpath('//div[@class="transaction"]/div/ul/li/text()').extract()[2]  # 上架时间
        item['sold_price_per'] = response.xpath('//div[@class="price"]/b/text()').extract()[0]  # 售出单价
        deal_date = response.meta['deal_date']  # 售出日期
        item['sold_date'] = deal_date.replace('.', '-')
        item['finish'] = False
        yield item