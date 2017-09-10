#encoding:utf8
# 删除微博

import re, requests, time
import urllib3, certifi
import urllib3.contrib.pyopenssl

# 证书认证
urllib3.contrib.pyopenssl.inject_into_urllib3()
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

# 爬取关键参数用的url
url = 'https://weibo.com/5872999549/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1'
# 提交删除请求的url
action_url = 'https://weibo.com/aj/mblog/del?ajwvr=6'

cookie = {'Cookies':'SINAGLOBAL=729242243553.1565.1505018913651; _s_tentry=-; Apache=1040190204990.0547.1505031774250; ULV=1505031774294:2:2:2:1040190204990.0547.1505031774250:1505018913712; login_sid_t=c18b7c7c64b34e44e0ff85b6de28c54e; UOR=jp.tingroom.com,widget.weibo.com,login.sina.com.cn; SSOLoginState=1505038881; SCF=AmORMVNPTscaOPcFLwW7li7FEtCMzxlRSKWgkmAzXDgoQKsYK1N4dnK5CusCnf2Kw_z940CMRzRVyKXi8ASrJmw.; SUB=_2A250sWJ8DeRhGeNG7FAY-SfJzzWIHXVXx9S0rDV8PUNbmtANLWj1kW9wTPuaTTPGH8rk2Gzr9ue0Qu9i7Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhwcXR6uSvYnrfYOoEzgsoj5JpX5K2hUgL.Fo-RS0z41K.fSh.2dJLoI0qLxK-LBoMLBKqLxK-L1h-L1hnLxKML1KBL1-qLxKBLBonLBoqLxK-L1hnLBK.LxK-LBKnL1h2t; SUHB=0bt8Z8uwmFV5Ai; ALF=1536574881; un=18813290826; wvr=6'}

headers = {'Referer':'https://weibo.com/5872999549/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1',
           'Cookie':cookie['Cookies'],
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}

count = 1
# 每次get页面有15条微博动态
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
