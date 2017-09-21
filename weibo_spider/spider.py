# -*- coding:utf-8 -*-

"""
爬虫爬取微博动态
"""

import requests
from lxml import etree


class Spider(object):

    def __init__(self, url, cook):
        self.url =  url
        self.cookies = cook
        self.content = ''


    def crawl(self):
    """爬取微博第一条动态，返回动态内容"""
    
        html = requests.get(self.url, cookies=self.cookies)
        selector = etree.HTML(html.content)
        path = '''//div[@class="c"]/div/span[@class="ctt"]'''
        self.content = selector.xpath(path)[0].xpath('string(.)')
        time = selector.xpath('//span[@class="ct"]/text()')[0]
        self.content = self.content + '\n' + time
        return self.content
