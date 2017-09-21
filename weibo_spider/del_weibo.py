# -*- coding:utf-8 -*-

"""
该模块可以批量删除微博动态
"""

import re
import time
import certifi
import urllib3
import urllib3.contrib.pyopenssl

import requests


# 证书认证
urllib3.contrib.pyopenssl.inject_into_urllib3()
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                           ca_certs=certifi.where())

# 微博个人主页url
url = 'xxx' 

# 提交删除请求到：action_url
action_url = 'https://weibo.com/aj/mblog/del?ajwvr=6'

cookie = {'Cookies':'xxx'}

headers = {'Referer':url,
           'Cookie':cookie['Cookies'],
           'User-Agent':'xxx'}

count = 1

# 删除150条微博动态
while count < 150:
    html = requests.get(url, cookies=cookie).text
    mids = re.findall(r'<a name=(\d*)', html, re.S)

    for each in mids:
        data = {'mid':'%s'%each}
        post = http.request('post', action_url, fields=data, headers=headers).data
        print u'删除第%s条'%count
        print u'成功！'
        count += 1
        time.sleep(1)
