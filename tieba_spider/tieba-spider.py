#encoding:utf8
# 多线程爬取百度贴吧每层楼的回帖信息

from lxml import etree
import requests, re, json
from multiprocessing.dummy import Pool

class Spider(object):
    # def __init__(self, total_pn):
    #     self.total_pn = total_pn

# 网页下载器
    def download(self, url):
        return requests.get(url).text

# 网页解析器
    def parse(self, html):
        data = []
        selector = etree.HTML(html)
        # 解析出所有楼层
        floors = selector.xpath('//*[@id="j_p_postlist"]/div')
        # 提取每层的回贴信息
        for each in floors:
            info = []
            info.append(each.xpath('div[2]/ul/li[3]/a/text()')[0])
            info.append(each.xpath('div[3]/div[1]/cc/div/text()')[0].replace(' ', ''))
            info.append(json.loads(each.xpath('@data-field')[0])['content']['date'])
            info.append(json.loads(each.xpath('@data-field')[0])['content']['post_no'])
            # info.append(each.xpath('div[3]/div[2]/div[1]/ul[1]/li[2]/span/text()')[0]) # 无法匹配，待解决
            data.append(info)
        return data

# 输出爬取结果
    def output(self, data):
        with open('tieba.txt', 'a') as fi:
            for each in data:
                fi.write('%s楼\n'%each[3])
                fi.write('回帖人：%s\n'%each[0].encode('utf8'))
                fi.write('内容：%s\n'%each[1].encode('utf8'))
                fi.write('回帖时间：%s\n\n'%each[2].encode('utf8'))

# 单线程时的翻页操作
    # def turn_page(self, current_url):
    #     pagenum = int(re.search(r'pn=(\d*)', current_url).group(1)) + 1
    #     current_url = re.sub(r'pn=\d*', 'pn=%d'%pagenum, current_url)
    #     return current_url

# 爬虫调度器
    def crawl(self, entry_url):
        
        # 单线程用代码
        # current_url = entry_url
        # for i in range(self.total_pn):
        #     html = self.download(current_url)
        #     data = self.parse(html)
        #     self.output(data)
        #     current_url = self.turn_page(current_url)
        
        # 多线程用代码
        html = self.download(entry_url)
        data = self.parse(html)
        self.output(data)

if __name__ == '__main__':
    # 多线程爬虫
    entry_url = 'http://tieba.baidu.com/p/3522395718?pn='
    url_li = []
    pool = Pool(4)
    tieba_spider = Spider()
    for pn in range(1,7):
        url_li.append(entry_url + str(pn))
    pool.map(tieba_spider.crawl, url_li)
    pool.close()
    pool.join()
