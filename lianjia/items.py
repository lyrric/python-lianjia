# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 小区信息
class CommunityItem(scrapy.Item):
    # define the fields for your item here like:
    code = scrapy.Field()  # 小区代码
    name = scrapy.Field()  # 小区名称
    selling_house_amount = scrapy.Field()  # 在售二手房数量
    sold_house_amount = scrapy.Field()  # 已成交房屋数量
    selling_avg_price = scrapy.Field()  # 售卖中的房屋单价
    sold_avg_price = scrapy.Field()  # 已售出的房屋单价
    new_house_amount = scrapy.Field()  # 新上架房屋数量
    district = scrapy.Field()  # 小区位置
    gmt_create = scrapy.Field()  # 采集时间
    version = scrapy.Field()  # 版本号


# 售卖中的房源信息
class SellingHouseItem(scrapy.Item):
    code = scrapy.Field()  # 房源code
    community_code = scrapy.Field()  # 小区code
    title = scrapy.Field()  # 房源title
    price = scrapy.Field()  # 挂牌价格
    price_per = scrapy.Field()  # 挂牌单价
    price_unit = scrapy.Field()  # 价格单位（万）
    type = scrapy.Field()  # 类型（两室一厅）
    size = scrapy.Field()  # 大小（59.5平米）
    on_sale_date = scrapy.Field()  # 上架时间
    deleted = scrapy.Field()  # 是否下架
    gmt_create = scrapy.Field()  # 采集时间
    gmt_update = scrapy.Field()  # 更新时间（最新一次采集时间）


# 售出的房源信息
class SoldHouseItem(scrapy.Item):
    code = scrapy.Field()  # 房源code
    community_code = scrapy.Field()  # 小区code
    title = scrapy.Field()  # 房源title
    selling_price = scrapy.Field()  # 挂牌价格
    sold_price = scrapy.Field()  # 成交价格
    sold_price_per = scrapy.Field()  # 成交单价
    price_unit = scrapy.Field()  # 价格单位（万）
    type = scrapy.Field()  # 类型（两室一厅）
    size = scrapy.Field()  # 大小（59.5平米）
    on_sale_date = scrapy.Field()  # 上架时间
    deleted = scrapy.Field()  # 是否下架
    sold_date = scrapy.Field()  # 售出时间
    gmt_create = scrapy.Field()  # 采集时间