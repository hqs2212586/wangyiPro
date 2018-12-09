# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# 爬虫中间件直接注释

# class WangyiproSpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)

# 下载中间件
from scrapy.http import HtmlResponse   # 通过这个类实例化的对象就是响应对象
import time

class WangyiproDownloaderMiddleware(object):
    def process_request(self, request, spider):
        """
        可以拦截请求
        :param request:
        :param spider:
        :return:
        """
        return None

    def process_response(self, request, response, spider):
        """
        可以拦截响应对象（下载器传递给Spider的响应对象）
        :param request: 响应对象对应的请求对象
        :param response: 拦截到的响应对象
        :param spider: 爬虫文件中对应的爬虫类的实例
        :return:
        """
        # print(request.url + "这是下载中间件")
        # 响应对象中存储页面数据的篡改
        if request.url in ['http://news.163.com/domestic/', 'http://news.163.com/world/', 'http://war.163.com/', 'http://news.163.com/air/']:
            # 浏览器请求发送（排除起始url）
            spider.bro.get(url=request.url)
            # 滚轮拖动到底部会动态加载新闻数据，js操作滚轮拖动
            js = 'window.scrollTo(0, document.body.scrollHeight)'  # 水平方向不移动：0；竖直方向移动：窗口高度
            spider.bro.execute_script(js)  # 拖动到底部，获取更多页面数据
            time.sleep(2)  # js执行给页面2秒时间缓冲，让所有数据得以加载
            # 页面数据page_text包含了动态加载出来的新闻数据对应的页面数据
            page_text = spider.bro.page_source
            # current_url就是通过浏览器发起请求所对应的url
            # body是当前响应对象携带的数据值
            return HtmlResponse(url=spider.bro.current_url, body=page_text, encoding="utf-8", request=request)
        else:
            # 四个板块之外的响应对象不做修改
            return response   # 这是原来的响应对象



# 单独给UA池封装一个下载中间件的类
# 1.导包：UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import random

class RandomUserAgent(UserAgentMiddleware):   # 继承UserAgentMiddleware
    def process_request(self, request, spider):
        """每次拦截请求，都会从列表中随机抽选一个ua赋值给当前拦截的请求"""
        # 从列表中随机抽选出一个ua值
        ua = random.choice(user_agent_list)
        # 请求头信息设置，赋值随机抽取的ua（当前拦截请求ua写入操作）
        request.headers.setdefault('User-Agent', ua)


user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


# 批量对拦截的请求进行Ip更换
class Proxy(object):
    def process_request(self, request, spider):
        # 对拦截到的请求url进行判断（协议头到底是http还是https）
        # 代理IP对协议头有严格区分
        # request.url返回值形式：http://www.xxx.com/
        h = request.url.split(":")[0]   # 切割获取协议头
        if h == "https":
            ip = random.choice(PROXY_https)
            # 利用meta修改代理ip
            request.meta['proxy'] = 'https://' + ip
        else:
            ip = random.choice(PROXY_http)
            request.meta['proxy'] = 'http://' + ip


# 可被选用的代理IP——去www.goubanjia.com获取免费代理IP
PROXY_http = [
    '182.96.249.68:808',
    '120.76.77.152:9999',
]
PROXY_https = [
    '121.33.220.158:808',
    '117.163.157.56:8123',
]