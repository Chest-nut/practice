#coding=utf-8

'''
Created on 2017年8月12日

@author: Administrator
'''
import urllib2


class HtmlDownloader(object):
    
    
    def download(self, url):
        if url == None:
            return 
        response = urllib2.urlopen(url)
        if response.getcode() != 200:
            return
        return response.read()
    
    



