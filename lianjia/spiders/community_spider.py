import scrapy
import pymysql
import json
import logging
from lianjia.items import CommunityItem
from lianjia import settings

"""
爬取所有小区
先获取成都市所有区县列表，再遍历区县列表获取小区
"""
class CommunitySpider(scrapy.Spider):
    name = 'community'
    allowed_domains = ['cd.lianjia.com']

    start_urls = ['https://cd.lianjia.com/xiaoqu/']
    community_base_url = 'https://cd.lianjia.com'

    db = pymysql.connect(**settings.DB_CONFIG)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    version = 0

    def parse(self, response):
        sql = 'select version from version '
        self.cur.execute(sql)
        row = self.cur.fetchone()
        self.version = int(row['version']) + 1
        logging.info('当前版本号为:' + str(self.version))
        # 获取成都市所有区县列表
        city_urls = response.xpath('//div[@data-role="ershoufang"]/div/a/@href').extract()
        city_names = response.xpath('//div[@data-role="ershoufang"]/div/a/text()').extract()
        i = 0
        while i < len(city_urls):
            logging.info('正在解析'+city_names[i]+'，url='+city_urls[i])
            city_full_url = self.community_base_url + city_urls[i]
            yield scrapy.Request(url=city_full_url, meta={'base_url': city_full_url}, callback=self.parse_community_index)
            i += 1
        # 完成之后让version + 1
        self.cur.execute('update version set version = (version + 1) ')

    #  解析小区列表第一页，获取页数
    def parse_community_index(self, response):
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        dict_page_data = json.loads(page_data)
        base_url = response.meta['base_url']
        total_page = dict_page_data['totalPage']
        page = 1
        while page <= total_page:
            logging.info('正在解析第'+str(page)+'页，共'+str(total_page)+'页')
            yield scrapy.Request(url=base_url+'/pg'+str(page), callback=self.parse_community)
            page += 1

    #  解析小区列表页
    def parse_community(self, response):
        codes = response.xpath('//li[@class="clear xiaoquListItem"]/@data-id').extract()  # 小区ID
        names = response.xpath('//div[@class="title"]/a/text()').extract()  # 小区名字
        selling_house_amount_list = response.xpath('//a[@class="totalSellCount"]/span/text()').extract()  # 在售二手房数量
        district_list = response.xpath('//div[@class="positionInfo"]/a[@class="district"]/text()').extract()  # 小区位置

        i = 0
        while i < len(codes):
            item = CommunityItem()
            item['code'] = codes[i]
            item['name'] = names[i]
            item['selling_house_amount'] = selling_house_amount_list[i]
            item['district'] = district_list[i]
            item['version'] = self.version
            yield item
            i += 1
