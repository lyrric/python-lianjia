# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommunityItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # 小区ID
    name = scrapy.Field()  # 小区名称
    selling_count = scrapy.Field()  # 在售二手房数量
    sold_avg_price = scrapy.Field()  # 上月二手房参考均价
    district = scrapy.Field()  # 小区位置
    pass
