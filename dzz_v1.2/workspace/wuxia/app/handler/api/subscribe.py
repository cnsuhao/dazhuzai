#coding:utf8
'''
Created on 2014-6-18

Copyright 2014 www.9miao.com
'''
from app.models import role, equipment, arena
from app.configdata import msgconfig
from app.handler.service import serviceHandle,wservice
from app.core.charater import Charater
import datetime

@serviceHandle("subscribe")
def subscribe(openid,request):
    """生成用户,用户关注
    """
    try:
        weiuser = role.Role.objects.get(openid=openid)
    except:
        weiuser = None
    #如果已经关注过
    if weiuser:
        #if weiuser.nickname:#如果已经取名
        #player = Charater(weiuser)
        #player.addRoleMessage(["欢迎回来！！！"])
        #player.model.save()
        return wservice.call("nowplot",openid,request)
    else:
        #如果没关注过
        weiuser = role.Role(openid=openid,subscribe_time=datetime.datetime.now())
        weiuser.save()
    player = Charater(weiuser)
    player.plot.notice("subscribe")
    player.model.save()
    return {"result":True,"data":""}
    
@serviceHandle("unsubscribe")
def unsubscribe(openid,msg):
    """取消订阅
    """
    try:
        try:
            weiuser = role.Role.objects.filter(openid=openid)
            weiuser.delete()
        except:
            pass
        try:
            equipment.Equipment.objects.filter(openid__startswith=openid).delete()
        except:
            pass
        # try:
        #     arena.Arena.objects.get(openid=openid).delete()
        # except:
        #     pass
        # try:
        #     arena.ArenaLog.objects.get(openid=openid).delete()
        # except:
        #     pass
        try:
            role.Share.objects.get(openid=openid).delete()
        except:
            pass
    except:
        weiuser = None
    return {"result":True,"data":""}

def checkNickname(nickname):
    """
    """
    print len(nickname)
    if len(nickname)>20 or len(nickname)<2:
        return False
    try:
        weiuser = role.Role.objects.get(nickname=nickname)
    except:
        weiuser = None
    if weiuser:
        return False
    return True
    
@serviceHandle("nickname")
def setNickName(openid,request):
    """
    """
    weiuser = role.Role.objects.get(openid=openid)
    if not checkNickname(request):
        return {"result":True,"data":msgconfig.getMsgFormat("illegal_name")}
    weiuser.nickname = request
    player = Charater(weiuser)
    player.plot.notice("subscribe")
    player.model.save()
    return {"result":True,"data":""}
    
@serviceHandle("nowplot")
def nowplot(openid,request):
    """获取当前剧情信息
    """
    weiuser = role.Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.plot.getNowPlotDesc()
    player.model.save()
    return {"result":True,"data":info}
    
    