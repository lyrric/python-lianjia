
from scrapy.cmdline import execute
import os
import sys

# 添加当前项目的绝对地址
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 执行爬取挂牌中的房源
execute(['scrapy', 'crawl', 'selling_house'])