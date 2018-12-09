# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from wangyiPro.items import WangyiproItem
from scrapy_redis.spiders import RedisSpider


# class WangyiSpider(scrapy.Spider):
class WangyiSpider(RedisSpider):
    name = 'wangyi'
    # allowed_domains = ['news.163.com']
    # start_urls = ['https://news.163.com/']
    redis_key = 'wangyi'

    def __init__(self):
        # 实例化浏览器对象(保证只会被实例化一次)
        self.bro = webdriver.Chrome(executable_path='/Users/hqs/ScrapyProjects/wangyiPro/wangyiPro/chromedriver')

    def closed(self, spider):
        # 必须在整个爬虫结束后关闭浏览器
        print('爬虫结束')
        self.bro.quit()   # 浏览器关闭

    def parse(self, response):
        lis = response.xpath('//div[@class="ns_area list"]/ul/li')
        # 获取指定的四个列表元素（国内3、国际5、军事6、航空7）
        indexes = [3, 4, 6, 7]
        li_list = []   # 四个板块对应的li标签对象
        for index in indexes:
            li_list.append(lis[index])

        # 获取四个板块中的超链和文字标题
        for li in li_list:
            url = li.xpath('./a/@href').extract_first()
            title = li.xpath('./a/text()').extract_first()   # 板块名称

            """对每一个板块对应url发起请求，获取页面数据"""
            # 调用scrapy.Request()方法发起get请求
            yield scrapy.Request(url=url, callback=self.parseSecond, meta={'title': title})

    def parseSecond(self, response):
        """声明回调函数"""
        # 找到页面中新闻的共有标签类型，排除广告标签
        # print(response.text)
        div_list = response.xpath('//div[@class="data_row news_article clearfix "]')  # 注意类最后有一个空格
        # print(len(div_list))   # 非空则验证xpath是正确的且动态页面加载到了响应中
        for div in div_list:
            # 文章标题
            head = div.xpath('.//div[@class="news_title"]/h3/a/text()').extract_first()
            # 文章url
            url = div.xpath('.//div[@class="news_title"]/h3/a/@href').extract_first()
            # 缩略图
            imgUrl = div.xpath('./a/img/@src').extract_first()
            # 发布时间和标签:提取列表中所有的元素
            tag = div.xpath('.//div[@class="news_tag"]//text()').extract()

            # 列表装化为字符串
            tags = []
            for t in tag:
                t = t.strip(' \n \t')   # 去除空格 \n换行 \t相当于tab
                tags.append(t)   # 重新装载到列表中
            tag = "".join(tags)

            print(head+':'+url+':'+imgUrl+':'+tag)

            # 获取meta传递的数据值
            title = response.meta['title']

            # 实例化item对象,将解析到的数据值存储到item对象中
            item = WangyiproItem()
            item['head'] = head
            item['url'] = url
            item['imgUrl'] = imgUrl
            item['tag'] = tag
            item['title'] = title

            # 对url发起请求，获取对应页面中存储的新闻内容数据
            yield scrapy.Request(url=url, callback=self.getContent, meta={"item":item})

    def getContent(self, response):
        """新闻内容解析的回调函数"""
        # 获取传递过来的item对象
        item = response.meta['item']

        # 解析当前页码中存储的页面数据
        # 由于新闻的段落可能有多个，每个段落在一个p标签中。因此使用extract()方法
        content_list = response.xpath('//div[@class="post_text"]/p/text()').extract()

        # 列表转字符串（字符串才能保持在item对象中）
        content = "".join(content_list)
        item["content"] = content

        # item对象提交给管道
        yield item













