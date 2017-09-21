# -*- coding:utf-8 -*-

"""
微博小助手：指定1名关注的用户，当其更新微博动态时，
发送邮件到指定邮箱。
"""

import os
import time

from spider import Spider
from mailhelper import Mailhelper


class Helper(object):

    def __init__(self, url, cook):
        self.spider = Spider(url, cook)
        self.content = ''
        self.mail_helper = Mailhelper()


    def refresh(self):
    """重新抓取网页内容"""
    
        self.content = self.spider.crawl()


    def is_new_msg(self):
    """判断抓取的内容是否为最新动态"""
    
        if os.path.exists('weibo.txt'):
            with open('weibo.txt', 'r') as fi:
                # 这里的split作用是去除微博中的时间信息，避免误判旧消息为新消息
                txt_content = '\n'.join(fi.read().split('\n')[:-1])
                new_content = '\n'.join(self.content.encode('utf8').split('\n')[:-1])
                if new_content is txt_content:
                    return False
                else:
                    return True
        else:
            return True


    def send_mail(self):
    """发送邮件到指定邮箱"""
    
        to_list = ['383105690@qq.com']  # 接收方邮箱
        sub = u'微博更新'               # 邮件标题
        if self.mail_helper.send_mail(to_list, sub, self.content):
            print u'发送成功！'
        else:
            print u'发送失败！'


if __name__ == '__main__':

    # 被关注对象的微博主页url（手机版微博）
    url = 'http://weibo.cn/u/2862532004'
    cook = {'Cookie':'''xxx'''}
    helper = Helper(url, cook)

    while True:
        # 刷新抓取数据
        helper.refresh()
        # 如果抓取的内容为新内容，将内容写入文件中，并发送邮件
        if helper.is_new_msg():
            with open('weibo.txt', 'w') as fi:
                fi.write(helper.content.encode('utf8'))
            helper.send_mail()
        else:
            print 'pass'
        time.sleep(10)
