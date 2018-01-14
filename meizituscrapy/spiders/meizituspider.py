# -*- coding: utf-8 -*-
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.shell import inspect_response
from meizituscrapy.items import MeizituscrapyItem
import re
import json
import pymysql
from meizituscrapy import settings
# 用XPATH解析所有RESPONSE
'''
test git
'''


class MeizituSider(CrawlSpider):
    name = "meizitu"

    allowed_domains = [
        "www.meizitu.com",
    ]
    start_urls = [
        "http://www.meizitu.com/",
    ]
    rules = (

        # 定义 follows= True 才会不断探索新URL
        # Rule(LinkExtractor(allow='http://mebook.cc/([\d]+).html'), callback='parse_detail'),
        Rule(LinkExtractor(allow='http://www.meizitu.com/a/more_([\d]+).html'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield Request(self.start_urls[0])

    def parse_item(self, response):
        for li in response.xpath('//ul[@class="wp-list clearfix"]/li/div/h3/a/@href'):
            yield Request(li.extract(), callback=self.parse_detail)

    def parse_detail(self, response):
        item = MeizituscrapyItem()
        image_urls = []
        for image_url in response.xpath('//img/@src'):
            image_urls.append(image_url.extract())
        item['image_urls'] = image_urls
        yield item
