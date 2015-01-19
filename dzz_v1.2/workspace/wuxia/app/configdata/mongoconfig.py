#coding:utf-8
'''
Created on 2014-7-21

Copyright 2014 www.9miao.com
'''
import mongoengine


def init_Mongo_Conns():
    import globalconfig
    mongoengine.connect(globalconfig.MONGO_DB,host=globalconfig.MONGO_HOST)
    