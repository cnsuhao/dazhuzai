#coding:utf8
'''
Created on 2014-6-18

Copyright 2014 www.9miao.com
'''

from gfirefly.dbentrust.util import ReadDataFromDB

MSG = {"not_scene_info":"场景信息不存在",
       "not_scene_exit":"那个方向没有出口",
       "not_equipment_exist":"没有[{equipment}]这个装备",
       "illegal_name":"角色名以及存在"
       }

def MSGConfig():
    pass
#     global MSG
#     resultlist = ReadDataFromDB('gamedata_messages')
#     for msg in resultlist:
#         MSG[msg['msgid']]=msg['message']

def getMsgFormat(msgkey,**kw):
    """获取消息格式
    """
    global MSG
    template = MSG.get(msgkey)
    if not template:
        return ""
    return template.format(**kw)


