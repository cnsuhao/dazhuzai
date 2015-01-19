#coding:utf8
'''
Created on 2014-6-23

Copyright 2014 www.9miao.com
'''
from app.configdata import msgconfig
from app.handler.service import serviceHandle
from app.models.role import Role
from app.core.charater import Charater

@serviceHandle("current")
def current(openid,request):
    """获取当前场景信息
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.postion.getSceneDesc()
    player.model.save()
    print info
    return {"result":True,"data":info}

@serviceHandle("npc")
def getNpcList(openid,request):
    """获取当前NPC列表
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.plot.notice('npc')
    player.model.save()
    return {"result":True,"data":""}
 
@serviceHandle("talkto")
def talkToNPC(openid,request):
    """与NPC进行交谈
    """
    npcid = request.replace("交谈", "").strip()
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    player.plot.notice('talkto',npcid=npcid)
    player.model.save()
    return {"result":True,"data":""}

@serviceHandle("proceed")
def proceed(openid,request):
    """继续
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info =player.plot.notice('proceed')
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("lookover")
def lookover(openid,request):
    """查看
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info =player.plot.notice('lookover')
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("go")
def go(openid,request):
    """前往
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info =player.plot.notice('go')
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("export_north")
def gotoExportNorth(openid,request):
    """向北走
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.postion.moveTo("north")
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("export_south")
def gotoExportSouth(openid,request):
    """向南走
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.postion.moveTo("south")
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("export_west")
def gotoExportWest(openid,request):
    """向西走
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.postion.moveTo("west")
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("export_east")
def gotoExportEast(openid,request):
    """向东走
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.postion.moveTo("east")
    player.model.save()
    return {"result":True,"data":info}
    
    
    
    
