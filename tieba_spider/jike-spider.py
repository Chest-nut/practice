#encoding:utf-8
# 爬取极客学院前n页课程信息

# from __future__ import print_function
import re, requests
import json

class Spider(object):
    def __init__(self, entry_url, total_pages):
        self.current_url = entry_url + '?pageNum=1'
        self.pagenum = 1
        self.total_pages = total_pages
        self.data = []

# 切换到下一页
    def turn_page(self):
        if self.pagenum < self.total_pages:
            self.pagenum += 1
        else:
            return 'no more pages'
        self.current_url = re.sub(r'\?pageNum=\d+', '?pageNum='+str(self.pagenum), self.current_url)

# 收集相关信息
    def collect_info(self, html):
        # 将所有课程的代码保存到一个列表
        courses = re.findall(r'<div class="lesson-infor".*?<div class="lessonicon-box">', html, re.S)
        # 提取每个课程的信息
        for each in courses:
            info = []
            # 提取课程标题，用 re.sub()方法去除所有空白符
            info.append(re.sub(r'\s', '', re.search(r'<h2 class="lesson-info-h2"><a href.*?>(.*?)</a></h2>', each, re.S).group(1)))
            # 提取课程概述
            info.append(re.sub(r'\s', '', re.search(r'<p style=.*?>(.*?)</p>', each, re.S).group(1)))
            # 提取课程时长、等级、学习人数
            li = re.findall(r'<em.*?>(.*?)</em>', each, re.S)
            info.extend( [re.sub(r'\s', '',li[0]),
                          re.sub(r'\s', '',li[1]),
                          re.sub(r'\s', '',li[2])] )
            # 将课程信息存入总列表
            self.data.append(info)

# 将所有课程信息写入jike.txt文件中
    def save_info(self):
        with open('jike.txt', 'w') as fi:
            for each in self.data:
                fi.write('标题：%s\n'%each[0].encode('utf8'))
                fi.write('课程概述：%s\n'%each[1].encode('utf8'))
                fi.write('时长：%s\n'%each[2].encode('utf8'))
                fi.write('等级：%s\n'%each[3].encode('utf8'))
                fi.write('学习人数：%s\n\n'%each[4].encode('utf8'))

# 爬虫主调度器
    def crawl(self):
        # 循环次数为爬取网页的总页数
        for i in range(self.total_pages):
            # 下载当前页面代码
            html = requests.get(self.current_url)
            # 提取出有用部分
            main_html = re.search(r'<div class="lesson-list"(.*?)<!--list end-->', html.text, re.S).group(1)
            # 收集当前页所有课程信息
            self.collect_info(main_html)
            # 切换下一页
            self.turn_page()

        # 将课程信息保存到文件中
        self.save_info()

if __name__ == '__main__':
    entry_url = 'http://www.jikexueyuan.com/course/python/'
    spider = Spider(entry_url, 4)   # 需要参数：入口url、需爬取的总页数
    spider.crawl()