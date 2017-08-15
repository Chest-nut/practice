#coding=utf-8

'''
Created on 2017年8月12日

@author: Administrator
'''
from bs4 import BeautifulSoup
import re


class HtmtParser(object):
    
    def _get_new_urls(self, url, soup):
        urls = set()
        links = soup.find_all('a', href = re.compile(r'/item/.*'))
        for link in links:
            urls.add(re.sub(r'/item/.*', link['href'], url))    
        return urls
    
    def _get_new_data(self, url, soup):
        res_data = {}
        
        res_data['url'] = url
        
        title_node = soup.find('dd', class_ = "lemmaWgt-lemmaTitle-title").find('h1')
        res_data['title'] = title_node.get_text()
        
        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        
        return res_data
    
    
    def parse(self, url, response):
        soup = BeautifulSoup(response, 'html.parser', from_encoding = 'utf-8')
        new_urls = self._get_new_urls(url, soup)
        new_data = self._get_new_data(url, soup)        
        return new_urls,new_data 
    
    



