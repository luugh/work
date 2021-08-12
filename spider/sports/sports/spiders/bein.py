# -*- coding: utf-8 -*-
import scrapy

# selenium相关库
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

# scrapy 信号相关库
from scrapy.utils.project import get_project_settings
# 下面这种方式，即将废弃，所以不用
# from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# scrapy最新采用的方案
from pydispatch import dispatcher
from scrapy import Request

class BeinSpider(scrapy.Spider):
    name = 'bein'
    allowed_domains = ['https://www.beinsports.com/en/tv-guide']
    start_urls = ['https://www.beinsports.com/en/tv-guide']

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,  # enabled by default
        'DOWNLOADER_MIDDLEWARES': {
            # 代理中间件
            'BeinSpider.middlewares.ProxiesMiddleware': 400,
            # SeleniumMiddleware 中间件
            'BeinSpider.middlewares.SeleniumMiddleware': 543,
            # 将scrapy默认的user-agent中间件关闭
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

        }
    }

    def __init__(self, timeout=30,isLoadImage=True, windowHeight=None, windowWidth=None):
        # 从settings.py中获取设置参数
        self.mySetting = get_project_settings()
        self.timeout = self.mySetting['SELENIUM_TIMEOUT']
        self.isLoadImage = self.mySetting['LOAD_IMAGE']
        self.windowHeight = self.mySetting['WINDOW_HEIGHT']
        self.windowWidth = self.mySetting['windowWidth']
        # 初始化chrome对象
        self.browser = webdriver.Chrome()
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(900, 900)
        self.browser.set_page_load_timeout(self.timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, 25)  # 指定元素加载超时时间
        super(BeinSpider, self).__init__()
        # 设置信号量，当收到spider_closed信号时，调用mySpiderCloseHandle方法，关闭chrome
        dispatcher.connect(receiver=self.mySpiderCloseHandle,
                           signal=signals.spider_closed
                           )

        # 信号量处理函数：关闭chrome浏览器

    def mySpiderCloseHandle(self, spider):
        print(f"mySpiderCloseHandle: enter ")
        self.browser.quit()

    def start_requests(self):
        yield Request(
            url="https://www.amazon.com/",
            meta={'usedSelenium': True, 'dont_redirect': True},
            callback=self.parseIndexPage,
            errback=self.error
        )

    def parse(self, response):

        pass
