#coding=utf-8

''' 
Created on 2017年8月12日

@author: Administrator
'''
from baike_spider import url_manager, html_downloader, html_parser,\
    html_outputter

class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManger()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmtParser()
        self.outputter = html_outputter.HtmlOutputter()
    
    def craw(self, entry_url):
        self.urls.add_new_url(entry_url)
        count = 1
        
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' %(count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputter.collect_data(new_data)
                
                if count == 20:
                    break
                count = count + 1
            except:
                print 'craw failed'
            
        self.outputter.output_html()
    
    



if __name__ == '__main__':
    entry_url = 'https://baike.baidu.com/item/Python'
    obj_spider = SpiderMain()
    obj_spider.craw(entry_url)