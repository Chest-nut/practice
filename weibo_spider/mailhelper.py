# -*- coding:utf-8 -*-

"""
该模块用于发送邮件
"""

import smtplib
from email.mime.text import MIMEText


class Mailhelper(object):
    """
    实现发送邮件的功能
    """
    
    def __init__(self):
        self.mail_host="smtp.qq.com"         # 设置服务器
        self.mail_user="xxx@qq.com"          # 用户名
        self.mail_pass="zfjatwahrljfcaeb"    # 第三方授权码


    def send_mail(self,to_list,sub,content):
        me = "weibo-helper" + "<"+self.mail_user+">"  # 发件人昵称 + 邮箱地址
        msg = MIMEText(content,_subtype='plain',_charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP_SSL()
            server.connect(self.mail_host, 465)
            server.login(self.mail_user,self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except Exception, e:
            print e
            return False
