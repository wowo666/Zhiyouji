# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Zhiyouji.items import ZhiyoujiItem
import time
from scrapy_redis.spiders import RedisCrawlSpider

class ZhiyoujiSpider(RedisCrawlSpider):
    name = 'zhiyouji'

    # allowed_domains = ['jobui.com']
    # start_urls = ['http://www.jobui.com/cmp']

    # 动态允许域
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(ZhiyoujiSpider, self).__init__(*args, **kwargs)
    # redis key
    redis_key = 'zhiyouji'

    rules = (
        # 详情页
        Rule(LinkExtractor(allow=r'company/\d+/$'), callback='parse_item'),
        # 翻页列表
        # Rule(LinkExtractor(allow=r'/cmp\?n=\d+#listInter'),follow=True),
        Rule(LinkExtractor(allow=r'/cmp\?n=\d+#listInter'),follow=True),
    )


    def parse_item(self, response):
        # print(response.url,"++++++++++++++")
        # 创建item对象
        item = ZhiyoujiItem()
        # 采集源
        item['datasource'] = response.url
        # 采集时间
        item['timestamp'] = time.time()
        # 企业名称
        item['company_name'] = response.xpath('//*[@id="companyH1"]/a/text()').extract_first()
        # 浏览人数
        item['views'] = response.xpath('//div[@class="grade cfix sbox"]/div[1]/text()').extract_first().split('人')[0].strip()
        # 企业性质
        item['category'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[1]/text()').extract_first().split('/')[0].strip()
        # 规模
        item['number'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[1]/text()').extract_first().split('/')[-1].strip()
        # 行业
        item['industry'] = response.xpath('//dl[@class="j-edit hasVist dlli mb10"]/dd[2]/a/text()').extract_first()
        # 公司简介
        item['desc'] = ''.join(response.xpath('//div[@class="cfix fs16"]/p/text()').extract())

        # 好评度
        item['praise'] = response.xpath('//div[@class="swf-contA"]/div/h3/text()').extract_first()
        # 薪资
        item['salary'] = response.xpath('//div[@class="swf-contB"]/div/h3/text()').extract_first()

        #  融资信息列表
        data_list = []
        node_list = response.xpath('//div[@class="jk-matter jk-box fs16"]/ul[@class="col-informlist"]/li')
        for node in node_list:
            temp = {}
            temp['time'] = node.xpath('./span[1]/text()').extract_first()
            temp['status'] = node.xpath('./h3/text()').extract_first()
            temp['amount'] = node.xpath('./span[2]/text()').extract_first()
            temp['investor'] = node.xpath('./span[3]/text()').extract()
            data_list.append(temp)
        item['finance_info'] = data_list

        # 排名列表
        rank_list = []
        for node in response.xpath('//div[@class="right-side"]/div[1]/div'):
            temp = {}
            key = node.xpath('./a/text()').extract_first()
            temp[key] = node.xpath('./span[2]/text()').extract_first()
            rank_list.append(temp)
        item['rank'] = rank_list

        # 地址
        item['address'] = response.xpath('//dl[@class="dlli fs16"]/dd[1]/text()').extract_first()
        # 联系方式
        item['contact'] = response.xpath('//div[@class="j-shower1 dn"]/dd/text()').extract_first()
        if item['contact'] != None:
            item['contact'] = item['contact'].replace('\xa0','')

        yield item