#encoding:utf8
# 爬虫类

import requests
from lxml import etree
# from multiprocessing.dummy import Pool

class Spider(object):
    def __init__(self, url, cook):
        self.url =  url
        self.cookies = cook
        self.content = ''

# 爬取微博第一条动态，返回动态内容
    def crawl(self):
        html = requests.get(self.url, cookies=self.cookies)
        selector = etree.HTML(html.content)
        self.content = selector.xpath('''//div[@class="c"]/div/span[@class="ctt"]''')[0].xpath('string(.)')
        time = selector.xpath('//span[@class="ct"]/text()')[0]
        self.content = self.content + '\n' + time
        return self.content
