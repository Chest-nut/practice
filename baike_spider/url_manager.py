#coding=utf-8

'''
Created on 2017年8月12日

@author: Administrator
'''


class UrlManger(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
    
    def add_new_url(self, url):
        if url == None:
            return
#         if url not in (self.new_urls | self.old_urls):
#             self.new_urls.add(url)
        self.new_urls.add(url)
    
    
    def has_new_url(self):
        if len(self.new_urls) > 0:
            return True
        return False

    
    def get_new_url(self):
        url = self.new_urls.pop()
        self.old_urls.add(url)
        return url

    
    def add_new_urls(self, urls):
        if len(urls) == 0:
            return
        for url in urls:
            self.new_urls.add(url)
    
    
    
    
    
    
    
    



