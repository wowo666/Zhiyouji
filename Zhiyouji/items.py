# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhiyoujiItem(scrapy.Item):
    # define the fields for your item here like:

    # 数据采集源
    datasource = scrapy.Field()
    # 数据采集时间
    timestamp = scrapy.Field()
    # 企业名
    company_name = scrapy.Field()
    # 浏览人数
    views = scrapy.Field()
    # 企业性质
    category = scrapy.Field()
    # 规模
    number = scrapy.Field()
    # 行业
    industry = scrapy.Field()
    # 公司简介
    desc = scrapy.Field()
    # 好评度
    praise = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 融资信息
    finance_info = scrapy.Field()
    # 排名
    rank = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 网址
    website = scrapy.Field()
    # 联系方式
    contact = scrapy.Field()
    pass
