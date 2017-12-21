# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup


def main():
    res = requests.get('http://www.shiyanlou.com/courses')
    soup = BeautifulSoup(res.text, 'lxml')
    # 课程链接都是这样的格式
    course_link = 'https://www.shiyanlou.com/courses/?category=all&course_type=all&fee=all&tag=all&page={}'
    page = soup.find('ul', {'class': 'pagination'})
    if len(page) < 1:
        print('未获得页面数')
        return None
    li_num = page.find_all('li')
    page_num = 0

    for i in li_num:
        try:
            li_num = int(i.find('a').get_text())
        except:
            li_num = 0
        if li_num > page_num:
            page_num = li_num
    for i in range(1, page_num + 1):
        print(course_link.format(i))


def get_course_link(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    courses = soup.find_all('div', {'class': 'col-md-3', 'class': 'col-sm-6', 'class': 'course'})
    for i in courses:
        try:
            title = i.find('div', {'class': 'course-name'}).get_text()
            study_num = i.find('span', {'class': 'course-per-num pull-left'}).get_text()
            study_num = re.sub("\D", "", study_num)
            link = i.find('a', {'class': 'course-box'}).get('href')
        except:
            return None
        print(title)
        print(study_num)
        print(link)


get_course_link('http://www.shiyanlou.com/courses')
# main()