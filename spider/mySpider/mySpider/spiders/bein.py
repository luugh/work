# -*- coding: utf-8 -*-
import scrapy


class BeinSpider(scrapy.Spider):
    name = 'bein'
    allowed_domains = ['www.beinsports.com/en/tv-guide']
    start_urls = ['http://www.beinsports.com/en/tv-guide']



    def parse(self, response):
        filename = "test.html"

        with open(filename, 'w',encoding='utf-8') as f:
            f.write(response.body.decode('utf-8'))
        # print('---------------')
        # print(response.body)
        # print('---------------')

