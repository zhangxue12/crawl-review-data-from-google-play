# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from gp.configs import *
import time

class ChromeDownloaderMiddleware(object):
    """docstring for ChromeDownloaderMiddleware"""
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless') #设置为无界面
        if CHROME_PATH:
            options.binary_location = CHROME_PATH
        if CHROME_DRIVER_PATH:
            self.driver = webdriver.Chrome(chrome_options=options,executable_path=CHROME_DRIVER_PATH)
        else:
            self.driver = webdriver.Chrome(chrome_options=options) #初始化chrome 驱动

    def __del__(self):
        self.driver.close()

    def process_request(self,request,spider):
        try:
            print('chrome driver begin...')
            
            #self.driver.set_window_size(1000,120000)
            self.driver.get(request.url) #获取页面连接内容
            
            newest = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[1]/div[1]/div[3]").click()
            time.sleep(5)
            newest = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()

            for i in range(0,25):
                self.driver.execute_script("window.scrollBy(0,2000)")
                #time.sleep(1)
                self.driver.execute_script("window.scrollBy(0,-1000)")
                time.sleep(1)
            #button = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click()
                try:
                    button = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click()
                    print("-----------------------------------------")
                except:
                    pass

            '''//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div[2]
                try:
                    
                    button = self.driver.find_element_by_xpath("//div[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span")
                    print(button.text())
                    button.click()
                except:
                    pass
            '''
            return HtmlResponse(url = request.url,body=self.driver.page_source,request=request,encoding='utf-8',status=200)
            #返回html数据
        except TimeoutException:
            return HtmlResponse(url=request.url,request=request,encoding='utf-8',status='500')
        finally:
            print("chrome driver end...")



class GpSpiderMiddleware(object):
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

        # Should return either None or an iterable of Request, dict
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


class GpDownloaderMiddleware(object):
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
