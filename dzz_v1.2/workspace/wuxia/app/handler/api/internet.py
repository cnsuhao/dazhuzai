#coding:utf8
'''
Created on 2014-6-19

Copyright 2014 www.9miao.com
'''
from app.configdata import msgconfig
from app.handler.service import serviceHandle
from pyquery import PyQuery as pq

@serviceHandle("internethelp")
def intersearch(openid,request):
    """网络查询
    """
    ss = pq(url="http://www.baidu.com/s?wd=%s"%request)
    return {"result":True,"data":ss('#2').text()}