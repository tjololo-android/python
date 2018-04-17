# -*- coding: utf-8 -*-
import scrapy


class MyspiderSpider(scrapy.Spider):
    name = 'Myspider'
    allowed_domains = ['http://www.23us.com/class/']
    start_urls = ['http://www.x23us.com/class/1_1.html']

    def parse(self, response):
        pass
