# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging

import pymysql
from scrapy import signals

from lianjia import settings
from lianjia.items import CommunityItem
from lianjia.spiders.community_spider import CommunitySpider


class LianjiaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.engine_stopped, signal=signals.engine_stopped)
        return s

    def spider_opened(self):
        pass

    def spider_closed(self, spider, reason):
        logging.info("spider_closed------------------------------------")

    def engine_stopped(self):
        logging.info("engine_stopped-------------------------------------")

