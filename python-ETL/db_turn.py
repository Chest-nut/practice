#encoding:utf8

from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy import between
from sqlalchemy import Column, BigInteger, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import random

engine = create_engine("mysql+mysqldb://root:123456@127.0.0.1/python_etl?charset=utf8", echo=False)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()
# conn = engine.connect()

class Ipdata(Base):
    __tablename__ = "ipdata"
    id = Column(Integer, primary_key=True)
    startip = Column(BigInteger)
    endip = Column(BigInteger)
    address = Column(String(20))
    carrier = Column(String(80))

Base.metadata.create_all(engine)


# 将ip地址字符串转换成十进制长整型数字
def ip2int(ip):
    hexn = ''.join(['%02X' %long(i) for i in ip.split('.') ])
    return long(hexn, 16)


# 将十进制长整型数字转换成ip地址字符串
def int2ip(num):
    li = []
    d = 256*256*256
    while d > 0:
        n, num = divmod(num, d)
        li.append(str(n))
        d = d / 256
    ip = '.'.join(li)
    return ip


def insert_all():
    # 先把 ipdata.csv 文件中所有的IP地址转换成十进制后，再插入到数据库
    with open('./ipdata.csv', 'r') as fi:
        lines = fi.readlines()
    # 分批插入数据库，一次2000条
    for i in range(len(lines)/2000 + 1):
        rs = []
        for l in lines[i*2000:(i+1)*2000]:
            ls = l.split(',', 4)
            rs.append(dict(id=ls[0],startip=ip2int(ls[1]),endip=ip2int(ls[2]),address=ls[3],carrier=ls[4]))
        session.execute(Ipdata.__table__.insert(), rs)
    session.commit()

    # <-------------------------------------------------------------------------------------------->
            # sql = "INSERT INTO ipdata(startip,endip,address,carrier) VALUES(%s,%s,'%s','%s')" \
            #   %(ls[1],ls[2],u'中国',u'外国')    # 无法插入中文？
    # session.execute(sql)


# 无索引查找100条记录
def search_no_index():
    with open('./ipdata.csv', 'r') as fi:
        lines = fi.readlines()
    samples = map(lambda x:ip2int(x.split(',')[1]), random.sample(lines, 100))
    for samp in samples:
        sql = "SELECT * FROM ipdata WHERE %s BETWEEN startip AND endip" %samp
        session.execute(sql).first()


# 有索引查找100条记录
def search_has_index():
    with open('./ipdata.csv', 'r') as fi:
        lines = fi.readlines()
    samples = map(lambda x:ip2int(x.split(',')[1]), random.sample(lines, 100))
    for samp in samples:
        sql = "SELECT * FROM ipdata WHERE %s > startip ORDER BY startip DESC LIMIT 1" %samp
        session.execute(sql)
        # res = session.query(Ipdata).filter(samp > Ipdata.startip).order_by(Ipdata.startip.desc()).first()


# 使用union all将100条SQL语句同时查询，但查询速度没有预期的效果，有待研究
def search_union():
    with open('./ipdata.csv', 'r') as fi:
        lines = fi.readlines()
    samples = map(lambda x:ip2int(x.split(',')[1]), random.sample(lines, 100))
    sql_list = []
    sql = "SELECT {0}.* FROM(SELECT * FROM ipdata WHERE %s > startip ORDER BY startip DESC LIMIT 1) {0}"
    for i in range(100):
        sql_list.append(sql.format('t'+str(i)) %samples[i])
    sql = ' union all '.join(sql_list)
    t1 = time.time()
    session.execute(sql)
    t2 = time.time()
    print(t2 - t1)



if __name__ == '__main__':
    # t1 = time.time()
    # insert_all()
    # t2 = time.time()
    # print(t2 - t1)  # 23.4739999771s, 插入444963条记录

    # t1 = time.time()
    # search_no_index()
    # t2 = time.time()
    # print(t2 - t1)  # 67.9670000076s, 无索引查找100条记录

    # t1 = time.time()
    # search_has_index()
    # t2 = time.time()
    # print(t2 - t1)  # 1.5529999733s, 有索引查找100条记录

    # search_union()
    pass


