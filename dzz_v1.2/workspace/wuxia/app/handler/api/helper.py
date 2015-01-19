#coding:utf8
'''
Created on 2014-6-19

Copyright 2014 www.9miao.com
'''
from weiwuxia.configdata import msgconfig
from weiwuxia.handler.service import serviceHandle

@serviceHandle("help")
def helpme(openid,request):
    """查看帮助
    """
    return True,msgconfig.getMsgFormat("help_msg")