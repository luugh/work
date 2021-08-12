# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class SportsSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SportsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
from logging import getLogger
import time

class SeleniumMiddleware():
    # Middleware中会传递进来一个spider，这就是我们的spider对象，从中可以获取__init__时的chrome相关元素
    def process_request(self, request, spider):
        '''
        用chrome抓取页面
        :param request: Request请求对象
        :param spider: Spider对象
        :return: HtmlResponse响应
        '''
        print(f"chrome is getting page")
        # 依靠meta中的标记，来决定是否需要使用selenium来爬取
        usedSelenium = request.meta.get('usedSelenium', False)
        if usedSelenium:
            try:
                spider.browser.get(request.url)
                # 搜索框是否出现
                input = spider.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='nav-search-field ']/input"))
                )
                time.sleep(2)
                input.clear()
                input.send_keys("iphone 7s")
                # 敲enter键, 进行搜索
                input.send_keys(Keys.RETURN)
                # 查看搜索结果是否出现
                searchRes = spider.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@id='resultsCol']"))
                )
            except Exception as e:
                print(f"chrome getting page error, Exception = {e}")
                return HtmlResponse(url=request.url, status=500, request=request)
            else:
                time.sleep(3)
                # 页面爬取成功，构造一个成功的Response对象(HtmlResponse是它的子类)
                return HtmlResponse(url=request.url,
                                    body=spider.browser.page_source,
                                    request=request,
                                    # 最好根据网页的具体编码而定
                                    encoding='utf-8',
                                    status=200)
