import scrapy
import pymysql
from scrapy.utils.project import get_project_settings

from lianjia import settings
import json
import logging
from lianjia.items import SellingHouseItem

"""爬取房屋信息
"""
class SellingHouseSpider(scrapy.Spider):

    name = 'selling_house'

    base_url = 'https://cd.lianjia.com/ershoufang/'

    def __init__(self, name=None, db_password=None, **kwargs):
        if db_password is not None and db_password != '':
            settings_copy = get_project_settings()
            db_conf = settings_copy.get('DB_CONFIG')
            db_conf['password'] = db_password
            settings_copy.set('DB_CONFIG', db_conf)
        super().__init__(name, **kwargs)

    def start_requests(self):
        sql = '''
            select * from community where selling_house_amount != 0 and version = (select version from version) 
        '''
        db = pymysql.connect(**settings.DB_CONFIG)
        cur = db.cursor(cursor=pymysql.cursors.DictCursor)
        cur.execute(sql)
        rows = cur.fetchall()
        db.close()
        cur.close()

        for row in rows:
            yield scrapy.Request(url=self.base_url + 'c' + row['code'], meta={'code': row['code'], 'name': row['name']}, callback=self.parse_index)

    # 解析列表首页，获取列表页数
    def parse_index(self, response):
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()
        community_code = response.meta['code']
        community_name = response.meta['name']
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
        house_codes = response.xpath('//div[@class="title"]/a/@data-housecode').extract()
        if len(house_codes) == 0:
            house_codes = response.xpath('//div[@class="title"]/a/@data-lj_action_housedel_id').extract()
        for code in house_codes:
            yield scrapy.Request(url=self.base_url + str(code) + '.html', callback=self.parse_house_detail)

    # 解析房源详情
    def parse_house_detail(self, response):
        item = SellingHouseItem()

        item['code'] = response.xpath('//div[@class="box_col"]/a/@data-housedel_id').extract()[0]  # 房源code
        item['community_code'] = response.xpath('//div[@class="box_col"]/a/@data-resblock_id').extract()[0]  # 小区code
        price = response.xpath('//p[@class="red big"]/span[@data-mark="price"]/text()').extract()[0] # 价格
        item['price'] = price.replace('万', '')
        item['price_unit'] = '万'
        item['deleted'] = False

        item['title'] = response.xpath('//h3[@class="house_desc lazyload_ulog"]/text()').extract()[0]  # 标题
        item['title'] = item['title'].lstrip()
        item['title'] = item['title'].rstrip()
        item['title'] = item['title'].replace('\n', '')
        item['title'] = item['title'].replace('{', '')
        item['title'] = item['title'].replace('}', '')
        item['title'] = item['title'].replace('"', ' ')
        price = response.xpath('//ul[@class="house_description big lightblack lazyload_ulog"]/li/text()').extract()[0] # 单价(16,060元/平)
        price = price[0: price.find('元')]
        price = price.replace(',' '')
        item['price_per'] = price
        item['type'] = response.xpath('//div[@class="similar_data_detail"]/p/text()').extract()[2]  # 两室一厅
        item['size'] = response.xpath('//div[@class="similar_data_detail"]/p/text()').extract()[4]  # 大小

        on_sale_date = response.xpath('//ul[@class="house_description big lightblack lazyload_ulog"]/li/text()').extract()[1] # 上架时间
        on_sale_date = on_sale_date.replace('.', '-')
        item['on_sale_date'] = on_sale_date
        item['finish'] = False
        yield item