# 常用的Python爬虫库及脚本爬虫

## 一、相关理论知识

### 1.1 HTTP库

- requests – 人性化的HTTP请求库。
- urllib和urllib2 - Python2、Python3自带的http请求库
- grequests – requests 库 + gevent ，用于异步 HTTP 请求。
- httplib2 – 全面的 HTTP 客户端库。
- treq – 类似 requests 的Python API 构建于 Twisted HTTP 客户端之上。

---

### 1.2 HTML解析库

- BeautifulSoup – 以 Python 风格的方式来对 HTML 或 XML 进行迭代，搜索和修改。
- cssutils – 一个 Python 的 CSS 库。
- html5lib – 一个兼容标准的 HTML 文档和片段解析及序列化库。
- lxml – 一个非常快速，简单易用，功能齐全的库，用来处理 HTML 和 XML。
- re - 正则表达式，规则过于强大以至于难以操作

---

### 1.3 网站爬取库

- Scrapy – 一个快速高级的屏幕爬取及网页采集框架。
- Grab – 站点爬取框架。
- portia – Scrapy 可视化爬取。
- pyspider – 一个强大的爬虫系统。

Python第三方库太多，学习起来成本也极高，这里就挑几个使用较多的库进行详细介绍：

- HTTP库推荐使用requests，使用简单方便，示例代码如下（注释是输出结果）：

```
#文件名：requests_get.py
#使用前，sudo pip3 install --upgrade requests更新一次
import requests # 导入requests库
res = requests.get('http://www.shiyanlou.com')  # 发起get请求，将返回结果保存到res中
res.status_code  # 200
```

示例代码中使用的是requests的get请求，访问了实验楼的官网，打印出来的200是http的状态码200（200即success），说明成功访问了。

![scrapy-3-1](http://ov2hhj4hl.bkt.clouddn.com/scrapy-3-1.png)

- html分析库，推荐使用BeautifulSoup搭配lxml，非常方便和使用。下面这个示例是requests搭配BeautifulSoup，抓取实验楼官网的课程首页，将课程类型、学习人数并搭配课程名在终端显示出来，配上效果图：

```
#代码内不方便注释，注释以讲解的方式写在下面
#使用前：
    #sudo pip3 install --upgrade bs4
    #sudo pip3 install --upgrade lxml
#运行脚本命令：python3 requests_get_2.py
#文件名：requests_get_2.py
import requests
import re
from bs4 import BeautifulSoup
res = requests.get('https://www.shiyanlou.com/courses/')#get请求，将结果保存到res中
soup = BeautifulSoup(res.text, 'lxml')#将结果中的html页面，让BeautifulSoup利用lxml解析，保存到soup中
course = soup.find_all('div',{'class':'col-md-4','class':'col-sm-6','class':'course'})#查找class为col-md-4 col-sm-6 course的全部div标签，返回列表
for i in course:#循环从列表中，拿到每个课程的HTML代码
    title = i.find('div',{'class':'course-name'}).get_text()#获取课程标题
    study_people = i.find('span',{'class':'course-per-num','class':'pull-left'}).get_text()#获取课程的学习人数
    study_people = re.sub("\D", "", study_people)# 数字这里有太多的空格和回车，清理一下
    try:
        tag = i.find('span',{'class':'course-per-num','class':'pull-right'}).get_text()#查找课程类型，如果没有这行报错
    except:
        tag="课程"#上面报错，说明没有课程类型，只有普通课程没有，所以赋值课程
    print("{}    学习人数:{}    {}\n".format(tag, study_people, title,))#打印课程类型、学习人数、课程名
```

![scrapy-3-2](http://ov2hhj4hl.bkt.clouddn.com/scrapy-3-2.png)

这里开始讲解上面的代码块：

- 导入包，requests和re直接导入，BeautifulSoup是在bs4的包内，用 from import

- 实验楼全部课程的链接是 https://www.shiyanlou.com/courses/ ，用requests发起get请求，得到res(response的简写)

- res是整个响应，res.text则是html的源码，用BeautifulSoup调用lxml的解析库解析html源码

- 根据html的编写规律，可以发现每个课程就是一个特定的div块内

![scrapy-3-3](http://ov2hhj4hl.bkt.clouddn.com/scrapy-3-3.png)

共15个，使用BeautifulSoup的find_all()查找全部，得到一个15个元素的列表。需要注意的是，div类名有三个，不能合在一起写成 `soup.find_all('div',{'class':'col-md-4 col-sm-6 course'})` ，这样匹配出来的数据是空列表。

- 因为每个课程的div块内容是一致的，所以爬取的规则就可以是一样的，然后遍历列表，提取课程的课程名title、学习人数study_people和课程标签类型tag，下面分开讲解爬取规则，贴张图：

![scrapy-3-4](http://ov2hhj4hl.bkt.clouddn.com/scrapy-3-4.png)

- 课程名title，从图片中可以看到在 `div` 标签中，它的类名是 `course-name` ，照着上面的模仿着写则是 `i.find('div',{'class':'course-name'})` ，这样就可以找到标题的 `div` 标签并返回。然后用 `get_text()` 函数返回它的内容，也就是标签开始和标签结尾中间的文本。
- 学习人数study_people，也是在 `span` 标签中，但是和title不同，`span` 标签内除了有数字，还有一个 `i` 标签，但是 `i` 标签内部没有文本。所以，直接用 `get_text()` 是可以的，如果 `i` 标签内部有文本，还需要剔除。学习人数study_people的爬取规则则是 `i.find('span',{'class':'course-per-num','class':'pull-left'})` 。但是这样爬取出来的文本，有很多空格、回车和制表符tab，下面一行则是使用正则表达式提取数字。

- 提取有价值的数字，反向思考就是剔除非数字字符，复杂且简单点的方法是python的字符串操作函数replace()，但是有空格、回车和制表符，要写三个replace就比较繁琐。因为正则表通常被用来检索、替换那些符合某个模式(规则)的文本，而且正则里面有符号\D来表示非数字，使用re.sub(被替换字符，新字符，目标字符串)并赋值给原study_people就可以了。

- 最后就是课程标签类型的抓取。课分为训练营、会员和基础，一般普通是没有标签的，所以这里就有个判断，如果标签不存在，即为基础课，如果存在就抓存在的，看下html源码，爬取规则是 `i.find('span',{'class':'course-per-num','class':'pull-right'})` 。不过为了涉及下python的异常处理，这里将爬取规则和获取文本写在一起，如果标签不存在，语句会直接报错。

```
try:
    tag = i.find('span',{'class':'course-per-num','class':'pull-right'}).get_text()
except:
    tag="课程"
```

try里面的代码为可能报错代码，如果报错，则执行except里面的代码。当然，你可以定制异常来对不同异常做不同的处理。

- 最后，将课程类型、学习人数、课程名进行一个简单的排版，format()函数是字符串的函数，将参数匹配字符串的大括号，语法 `" {} [{} {}...] ".format(par, [par1, par2...])` 

网站爬取库太多，Scrapy当属盛名，不必多少，整个项目都是围绕Scrapy展开的。

---

## 二、本节总结

列举了一部分的第三方库，并举例说明了requests和BeautifulSoup的使用说明，主要围绕实验楼全部课程的第一页做了一个脚本爬虫，对库和Python的基础做了点讲解。下一节将延伸和拓展本节的脚本爬虫，使爬虫更强大，当然覆盖的面更广，以及涉及到的知识点会更多，当然也会倍儿有意思。