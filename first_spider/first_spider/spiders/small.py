#!/usr/bin env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-28 17:00:56

import scrapy
from ..items import FirstSpiderItem


class tubgua_spider(scrapy.Spider):
    # (required)爬虫名，scrapy list命令会列出name
    name = "pic_spider"
    #  (required)允许爬取的url域名，如果url中域名不是这段不进行爬取。这里是python列表类型，可以放多个链接
    allowed_domains = ["www.ivsky.com"]
    # (required)爬虫启动时会首先打开的url。这里是python的列表类型，可以放多个链接
    start_urls = ["http://www.ivsky.com/tupian/renwutupian/"]

    # parse方法，爬虫启动会自动调用爬虫类中的parse方法，传入response【页面加载成功后得到的数据】
    def parse(self, response):
        sspider = FirstSpiderItem()

        # '//ul[@class="ali"]/li/img/@src' = 当前页面中所有的class为ali的ul标签、
        # 下的li标签、里面所有的img标签、的src属性的值
        sspider['pic'] = response.xpath('//ul[@class="ali"]/li//img/@src').extract()
        return sspider
