# 简单Scrapy项目运行和剖析

## 一、项目运行

本节课程主要是运行已经写好的简单scrapy项目，查看图片效果。

1.训练营的基础项目都存放在github上了，使用终端在Desktop的目录下git下来即可：

```
git clone https://github.com/Vrolist/scrapy_spider.git
```

![scrapy-2-1](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-1.png)

2.终端中cd进到Scrapy_spider目录下的small_spider目录中去，使用命令：

`scrapy list` 查看爬虫项目中有多少个爬虫，界面会列出当前所有爬虫的名字。

![scrapy-2-2](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-2.png)

3.获得了爬虫名，直接使用爬虫命令运行：

```
scrapy crawl pic_spider
```

![scrapy-2-3](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-3.png)

当前爬虫是爬取指定url页面中的图片，并将图片保存到本地，看结果图。

![scrapy-2-4](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-4.png)

4.这里贴上原网页图片和网页源码图片进行对比：

![scrapy-2-5](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-5.png)

在class为ali的ul标签里面，有18个li标签，每个li里面都是div->a->img，这样就走到了img标签内，图片链接就是img标签的src属性了。

以上就是整个爬虫运行的过程，数据筛选就是将图片保存本地。

> 注意：地址就是你命令行所在的文件夹。你爬取的图片和截图不同，是因为页面会更新，具体的测试对比要用你实验时打开页面的图片和你爬取的图片对比。

---

## 三、项目详解

在解释Scrapy项目前，先讲讲Scrapy的运行机制，请看下图：

![scrapy-2-6](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-6.png)

1. 列表项爬虫启动，引擎(Engine)会将起始的url传入到调度器(Scheduler)
2. 列表项调度器(Scheduler)将url发给下载器(Download)，下载器(Download)发起网络请求并将得到的数据发给爬虫(Spider)进行分析
3. 列表项爬虫(Spider)开始分析数据，得到数据之后有两种情况：
    - 分析得到下一个链接，进一步调用调度器(Scheduler)对链接进行前面两步操作
    - 将分析得到的需要保存的数据，它们则被送到项目管道(Item Pipeline)那里，那是对数据进行后期处理（详细分析、过滤、存储等）的地方

以上就是Scrapy运行的顺序。现在开始贴代码解释这个简单Scrapy项目:

方便后面学习爬虫和管道代码，先贴上Items.py的代码。

```
# 这个是Item.py文件
import scrapy

class SmallSpiderItem(scrapy.Item):
    pic = scrapy.Field()  # 这个pic很重要的，后面使用必须一致，不然报错
```

爬虫的代码文件位于spider目录内(即上一小节的第三层)

![scrapy-2-7](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-7.png)

具体代码如下 `所有“#注释...”都是后加的代码的解释`：

```
#注释-这个是small.py文件
# -*- coding:utf-8 -*-
#注释-如果报中文编码错误，加上上面一行，或者去掉全部中文
import scrapy
from ..items import SmallSpiderItem

#注释-爬虫的类，必须继承scrapy.Spider
class tubagua_spider(scrapy.Spider):
    #注释-必须字段，爬虫名，scrapy list命令行会列出name
    name = "pic_spider"
    #注释-必须字段，允许的爬取的url域名，如果url中域名不是这段不进行爬取。这里是python的列表类型，可以放多个链接
    allowed_domains = ["www.ivsky.com"]
    #注释-必须字段，爬虫启动时首先打开的url。这里是python的列表类型，可以放多个链接
    start_urls = ["http://www.ivsky.com/tupian/renwutupian/"]


    #注释-parse方法，爬虫启动会自动调用爬虫类中的parse方法，传入response【页面加载成功后得到的数据】
    def parse(self, response):
        sspider = SmallSpiderItem()
        #注释-这里使用到了xpath对html进行分析，得到的结果赋值给我们定义的Item.py里面的类，pic必须一致，不然报错。后面会有一个章节详细介绍xpath，在这里简单翻译一下【没看懂没关系，可能是我解释不清楚】。
        #注释-'//ul[@class="ali"]/li//img/@src' = 当前页面中所有的class为ali的ul标签、下的li标签、里面的所有img标签、的src属性的值
        sspider['pic'] = response.xpath('//ul[@class="ali"]/li//img/@src').extract()
        # print(sspider['pic'],len(sspider['pic']))
        return sspider
```
以上就是spider目录（即上一小节的第三层）的全部代码了，因为 `__init__.py` 文件里面没有任何代码。

在spider目录下定义了一个small.py的爬虫，里面根据爬取url获得的response，从中分析到了页面中图片的图片，直接返回了我们定义好的Item项目。但是我们爬虫的代码并没有将图片保存至本地，那保存图片的操作是在哪里执行的？

这里呢就是分工操作，scrapy的顺序如下

![scrapy-2-8](http://ov2hhj4hl.bkt.clouddn.com/scrapy-2-8.png)

调度器和下载器都是直接使用的，爬虫是我们编写的爬取规则，项目管道也是我们自定义的，例如插入api、存入数据库、保存本地文件。

本项目中，图片的保存是项目管道 `pipeline.py` 的代码文件进行的操作，保存到当前命令行所在位置，下面贴上保存图片的代码(#注释...都是添加的解释代码，运行时最好全部删除)

```
#注释-这个是pipeline.py文件
import urllib

class SmallSpiderPipeline(object):
    def process_item(self, item, spider):
        #注释-item['pic']里面是一个列表，存放着18张图片的url链接
        for i in item['pic']:
            print(i)#注释-打印图片的url链接
            pic_name = i.split('/')[-1]
            #注释-使用urllib库里面的urlretrieve函数，前者是图片的完整路径，后者是图片的url路径
            urllib.request.urlretrieve(i,'z_p-'+pic_name)
        # return item
```

以上就是爬虫的98%的代码了。当然一个功能完善的爬虫还需要更多的设置，最后贴上 `settings.py`

```
#注释-这个是setting.py文件
BOT_NAME = 'small_spider'

SPIDER_MODULES = ['small_spider.spiders']
NEWSPIDER_MODULE = 'small_spider.spiders'

ROBOTSTXT_OBEY = True

#注释-以上部分是默认存在的，下面这个是添加的
#注释-ITEM_PIPELINES在这里是字典类型，后面的300是数值，1~1000范围内即可。【为了兼容性，ITEM_PIPELINES也可以是列表】
ITEM_PIPELINES = {
   'small_spider.pipelines.SmallSpiderPipeline': 300,
}
```

就目前的简单Scrapy爬虫项目而言，`settings.py` 不需要太多的设置，后面慢慢的涉及越来越复杂的网站时，则 `settings.py` 中就需要配置其他项，这个就到后面需要时再做介绍和学习。

---

## 本节总结

本节对Scrapy的运行顺序做了个介绍，并初步的涉及了爬虫和项目管道代码讲解和对Python一些数据类型的提及。后面几个小节会对Python的基础知识和http网络知识点做一个详述，希望能为基础薄弱的巩固基础，以便在后面的课程学习中可以更顺畅。