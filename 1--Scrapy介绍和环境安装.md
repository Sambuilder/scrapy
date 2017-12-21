# Scrapy介绍和环境安装

## Scrapy介绍

Scrapy，Python开发的一个快速,高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。

Scrapy吸引人的地方在于它是一个框架，任何人都可以根据需求方便的修改。它也提供了多种类型爬虫的基类，如BaseSpider、sitemap爬虫等，最新版本又提供了web2.0爬虫的支持。

---

## 环境的配置

实验楼的在线环境不包含Scrapy库的，我们需要自行安装Scrapy库。请先安装环境在继续后续课程学习，学习过程中请不要忘记保存环境。

```
sudo apt-get update  # 首先更新一下Ubuntu中的源
sudo apt-get install python3-lxml python3-dev libffi-dev libxml2-dev  #安装必备python的拓展库
```

![scrapy-1-1](http://ov2hhj4hl.bkt.clouddn.com/scrapy-1-1.png)

```
sudo pip3 install --upgrade pip #课程使用Python3，虚拟机自带的Python3的pip版本较低，先升级!
```

![scrapy-1-2](http://ov2hhj4hl.bkt.clouddn.com/scrapy-1-2.png)

```
sudo pip3 install scrapy #安装scrapy并更新
```

安装完成后查看scrapy版本号，输入命令 `scrapy version` 查看版本，本训练营课程使用的是1.3.2版本

![scrapy-1-3](http://ov2hhj4hl.bkt.clouddn.com/scrapy-1-3.png)

到目前为止，Scrapy已经安装成功了，使用命令cd进入到桌面 `cd Desktop` ，使用scrapy命令新建一个scrapy爬虫项目，命令行：`scrapy startproject first_spider`


此时桌面上就多有一个名为first_spider的文件夹

![scrapy-1-4](http://ov2hhj4hl.bkt.clouddn.com/scrapy-1-4.png)

---

## Scrapy项目文件介绍

初始化Scrapy项目中，各文件和文件夹的作用

![scrapy-1-5](http://ov2hhj4hl.bkt.clouddn.com/scrapy-1-5.png)


first_spider文件夹内，有一个scrapy.cfg配置文件和first_spider的文件夹

- 第一层[一级first_spider目录]:

    - scrapy.cfg：配置文件，不需要更改
    - first_spider文件夹：第二层解释

- 第二层[二级first_spider目录]：
    - `__init__.py` ：特定文件，指明二级first_spider目录为一个python模块
    - item.py：定义需要的item类【实验中需要用到】
    - pipeline.py：管道文件，传入item.py中的item类，清理数据，保存或入库
    - settings.py：设置文件，例如设置用户代理和初始下载延迟
    - spiders目录：第三层解释

- 第三层【spiders目录】
    - `__init__.py` :特定文件，指明二级first_spider目录为一个python模块
    - 这里是放自定义爬虫的py文件，负责从html中获得数据，传入上一层管道文件中进行数据清理

Scrapy环境的安装和Scrapy初始化项目的文件介绍就到这里，下一个实验会给出一个可以直接运行的爬虫项目，对目标网站进行数据抓取和保存，并带着大家详细的剖析。