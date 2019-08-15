import scrapy
import pymysql
from lianjia import settings
import json
import logging
from lianjia.items import HouseItem

"""爬取房屋信息
"""
class HourseSpider(scrapy.Spider):

    name = 'house'

    base_url = 'https://cd.lianjia.com/ershoufang/'
    db = pymysql.connect(**settings.DB_CONFIG)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)

    def start_requests(self):
        sql = 'select * from community where selling_count <> 0 '
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            yield scrapy.Request(url=self.base_url + 'c' + row['id'], meta={'id': row['id']}, callback=self.parse_index)

    # 解析列表首页，获取列表页数
    def parse_index(self, response):
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        community_id = response.meta['id']
        if page_data is None or len(page_data) == 0:
            total_page = 1
        else:
            page_data = page_data[0]
            dict_page_data = json.loads(page_data)
            total_page = dict_page_data['totalPage']
        page = 1
        while page <= total_page:
            logging.info('正在解析第' + str(page) + '页，共' + str(total_page) + '页')
            yield scrapy.Request(url=self.base_url + '/pg' + str(page) + 'c' + community_id,
                                 callback=self.parse_house_list)
            page = page + 1

    # 解析房源列表
    def parse_house_list(self, response):
        house_ids = response.xpath('//a[@class="LOGCLICKDATA "]/@data-lj_action_housedel_id').extract()
        for id in house_ids:
            yield scrapy.Request(url=self.base_url + str(id) + '.html', callback=self.parse_house_detail)

    # 解析房源详情
    def parse_house_detail(self, response):
        item = HouseItem()
        item['id'] = response.xpath(
            '//div[@class="btnContainer  LOGVIEWDATA LOGVIEW"]/@data-lj_action_resblock_id').extract()[0]  # 房源id
        item['community_id'] = response.xpath(
            '//div[@class="btnContainer  LOGVIEWDATA LOGVIEW"]/@data-lj_action_housedel_id').extract()[0]  # 小区id
        item['title'] = response.xpath('//h1[@class="main"]/text()').extract()[0]  # 标题
        item['price'] = response.xpath('//div[@class="price "]/span[@class="total"]/text()').extract()[0]  # 价格
        item['price_unit'] = response.xpath('//div[@class="price "]/span[@class="unit"]/span/text()').extract()[0]  # 价格单位（万）
        item['price_per'] = response.xpath('//span[@class="unitPriceValue"]/text()').extract()[0]  # 单价
        item['price_per_unit'] = response.xpath('//span[@class="unitPriceValue"]/i/text()').extract()[0]  # 单价单位(元/平米)
        item['type'] = response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract()[0]  # 两室一厅
        item['size'] = response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').extract()[0]  # 大小
        item['on_sale_date'] = response.xpath('//div[@class="transaction"]/div[@class="content"]/ul/li/span/text()').extract()[1]  # 上架时间
        yield item
