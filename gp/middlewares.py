# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#    def __init__(self):

# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from gp.configs import *
import time
import datetime
import pymongo

class ChromeDownloaderMiddleware(object):
    """docstring for ChromeDownloaderMiddleware"""
    def __init__(self):
        options=webdriver.ChromeOptions()
        #options.add_argument('--headless') #设置为无界面
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
            url_check=request.url
            url_check=url_check.split(".")
            #确定当前爬取的时哪一个app
            for item in url_check:
                if "zoom" == item:
                    db_name="Zoom"
                    break
                elif "alibaba" == item:
                    db_name="Ding_Talk"
                    break
                elif "apps" == item:
                    db_name="Google_Meet"
                    break
            #连接数据，查看最新的日期是何时
            client = pymongo.MongoClient("mongodb://7630:ais7630@localhost:27017/")
            db = client["7630_DB"]
            coll =db[db_name]  
            doc=coll.find()
            print(type(doc))
            for item in doc:
                obj=item
                break
            #如果数据库为空，则爬取很长时间
            if doc.count()==0:
                crawl_loop=300
            else:
                latest = obj.get("time")
                latest =latest.split("/")
                now_time=time.localtime()
                #计算出数据库已有数据和当前日期的差值
                cp_day = (now_time.tm_mon-int(latest[1]))*10+(now_time.tm_mday-int(latest[2]))
                crawl_loop = cp_day*2


            self.driver.get(request.url) #获取页面连接内容
            time.sleep(2)
            newest = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[1]/div[1]/div[3]").click()
            time.sleep(5)
            newest = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()

            #根据设定的爬取时间，通过拉动滚动条 和 点击 show more 爬取页面
            for i in range(0,crawl_loop):
                self.driver.execute_script("window.scrollBy(0,2000)")
                #time.sleep(1)
                self.driver.execute_script("window.scrollBy(0,-1000)")
                time.sleep(2)
            #button = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click()
                try:
                    button = self.driver.find_element_by_xpath("//*[@id='fcxH9b']/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div").click()
                    print("-----------------------------------------")
                except:
                    pass

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
