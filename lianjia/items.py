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

class HouseItem(scrapy.Item):
    id = scrapy.Field()  # 房源ID
    community_id = scrapy.Field()  # 小区ID
    title = scrapy.Field()  # 房源标题
    price = scrapy.Field()  # 价格
    price_unit = scrapy.Field()  # 价格单位（万）
    price_per = scrapy.Field()  # 单价
    price_per_unit = scrapy.Field()  # 单价单位(元/平米)
    type = scrapy.Field()  # 类型（两室一厅）
    size = scrapy.Field()  # 大小（59.5平米）
    on_sale_date = scrapy.Field()  # 上架时间
    gmt_create = scrapy.Field()  # 采集时间


