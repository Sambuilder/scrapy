# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib


class FirstSpiderPipeline(object):

    def process_item(self, item, spider):
        # item['pic']里面是一个列表，存放着18张图片的url链接
        for i in item['pic']:
            # 打印图片的url链接
            print(i)
            pic_name = i.split('/')[-1]
            # 使用urllib库里面的urlretrieve函数，前者是图片的完整路径。后者是图片的url路径
            urllib.request.urlretrieve(i, 'z_p-' + pic_name)
        # return item
