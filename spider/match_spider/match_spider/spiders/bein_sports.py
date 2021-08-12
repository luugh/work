# -*- coding: utf-8 -*-


import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.utils.project import get_project_settings
from scrapy import signals
from pydispatch import dispatcher

import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
parentPath = os.path.split(curPath)[0]
rootPath = os.path.split(parentPath)[0]
sys.path.append(rootPath)


class Bein_sportsSpider(scrapy.Spider):
    name = 'bein_sports'
    allowed_domains = ['beinsports.com']
    start_urls = ['https://www.beinsports.com/en/tv-guide']
    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'bein_sportsSpider.middlewares.ProxiesMiddleware': 400,
            'bein_sportsSpider.middlewares.SeleniumMiddleware': 543,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
        }
    }

    def __init__(self):
        # 从setting中获取设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        # 初始化chrome对象
        self.browser = webdriver.Chrome()
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)
        self.wait = WebDriverWait(self.browser, 25)
    #     super(beinSportsSpider, self).__init__()
    #     # 设置信号量，当收到spider_closed信号时，调用bein_sportsCloseHandle方法，关闭chrom
    #     dispatcher.connect(receiver=self.beinSportsSpiderCloseHandle,
    #                        signal=signals.spider_closed
    #                        )
    #
    # # 信号量处理函数：关闭chrom浏览器
    # def beinSportsSpiderCloseHandle(self, spider):
    #     print('beinSportsSpiderCloseHandle:enter')
    #     self.browser.quit()

    def parse(self, response):
        # start_urls = ['https://www.beinsports.com/en/tv-guide']
        url = 'https://www.beinsports.com/en/tv-guide'
        yield scrapy.Request(
            url=url,
            meta={'usedSelenium': True, 'dont_redirect': True},
            callback=self.parseIndexPage,
            errback=self.error
        )
