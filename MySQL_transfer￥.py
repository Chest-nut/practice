# -*- coding: utf-8 -*-
"""
Created on Fri Aug 04 21:28:13 2017

@author: Administrator

MySQL的简易账户转账操作

"""

import MySQLdb
import sys

class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn
    
    def check_user_available(self, user):
        cursor = self.conn.cursor()
        try:
            sql = "select * from user where userName=%s" % user
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账户%s不存在"%user)
        finally:
            cursor.close()
            
    def has_enough_money(self, user,money):
        cursor = self.conn.cursor()
        try:
            sql = "select * from user where userName=%s and money>%d" % (user, money)
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("账户%s余额不足"%user)
        finally:
            cursor.close()

    def reduce_money(self, user, money):
        cursor = self.conn.cursor()
        try:
            sql = "update user set money=money-%d where userName=%s" % (money, user)
            cursor.execute(sql)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("账户%s减款失败"%user)
        finally:
            cursor.close()

    def add_money(self, user, money):
        cursor = self.conn.cursor()
        try:
            sql = "update user set money=money+%d where userName=%s" % (money, user)
            cursor.execute(sql)
            rs = cursor.rowcount
            if rs != 1:
                raise Exception("账户%s加款失败"%user)
        finally:
            cursor.close()
        
    def transfer(self, source_user, target_user, money):
        try:
            self.check_user_available(source_user)
            self.check_user_available(target_user)
            self.has_enough_money(source_user,money)
            self.reduce_money(source_user, money)
            self.add_money(target_user, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback
            raise e

if __name__ == '__main__':
    source_user = '1'
    target_user = '2'
    money = 100
    
    conn = MySQLdb.Connect(host = '127.0.0.1', port = 3306, 
                           user = 'root', passwd = '123456', 
                           db = 'imooc', charset = 'utf8')
    tr_money = TransferMoney(conn)
    try:
        tr_money.transfer(source_user, target_user, money)
    except Exception as e:
        print '出现问题:' + str(e)
    finally:
        conn.close()
