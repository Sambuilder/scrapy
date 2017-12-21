import requests
import re
from bs4 import BeautifulSoup

# res = requests.get('http://www.shiyanlou.com')
# print(res.status_code)

res = requests.get('http://www.shiyanlou.com/courses')
# 使用BeautifuleSoup的lxml方式解析并保存到soup中
soup = BeautifulSoup(res.text, 'lxml')
# 查找clas为col-md-4 col-sm-6 course的全部div标签,返回列表
course = soup.find_all('div', {'class': 'col-md-3', 'class': 'col-sm-6', 'class': 'course'})
# print(course)
for i in course:
    # 获取课程标题
    title = i.find('div', {'class': 'course-name'}).get_text()
    # 获取课程人数
    study_people = i.find('span', {'class': 'course-per-num', 'class': 'pull-left'}).get_text()
    # 数字里有太多的空格和回车,清理一下
    study_people = re.sub('\D', "", study_people)
    try:
        #查找课程类型，如果没有这行报错`
        tag = i.find('span', {'class': 'course-money', 'class': 'pull-right'}).get_text()
    except:
        # 如果找不到课程类型标签,就赋值为课程
        tag = "课程"
    print("{}:\n课程名称: {}\n学习人数: {}".format(tag, title, study_people))