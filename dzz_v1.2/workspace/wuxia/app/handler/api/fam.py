#coding:utf-8
'''
Created on 2014-8-4

Copyright 2014 www.9miao.com
'''
from app.configdata import msgconfig
from app.handler.service import serviceHandle
from app.models.role import Role
from app.core.charater import Charater

@serviceHandle("famlist")
def famlist(openid,request):
    """获取当前可进行的副本列表
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.fam.getFamList()
    player.plot.notice('famlist')#通知查看了副本列表
    player.model.prev_command = "famlist"
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("enterfamid")
def enterFamId(openid,request):
    """进入副本
    """
    # try:
    #     fam_id = int(request)
    # except ValueError:
    #     return {"result":True,"data":"秘境序号有误"}
    fam_id = request.strip()
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    now_fam_id = player.fam.fam
    # if now_fam_id:
    #     info="当前已经在秘境中"
    # else:
    info = player.fam.enterFam(fam_id)
    player.plot.notice('enterfam',fam_id=fam_id)#通知进入了副本
    
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("enterfam")
def enterFam(openid,request):
    """进入副本
    """
    fam_id = request.replace("进入", "").strip()
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    now_fam_id = player.fam.fam
    # if now_fam_id:
    #     info="当前已经在秘境中"
    # else:
    info = player.fam.enterFam(fam_id)
    player.plot.notice('enterfam',fam_id=fam_id)#通知进入了副本

    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("challenge")
def challenge(openid,request):
    """挑战副本
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    fam_id = player.fam.fam
    fam_node = player.fam.famnode
    if not fam_id or not fam_node:
        info="当前不在秘境中"
    else:
        info = player.fam.challenge()
        player.plot.notice('challenge',fam_id=fam_id,fam_node=fam_node)#通知进行了副本战斗
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("exitfam")
def exitFam(openid,request):
    """挑战副本
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    fam_id = player.fam.fam
    if not fam_id:
        info = "当前不在秘境中"
    else:
        info = player.fam.exitFam()
        player.plot.notice('exitfam',fam_id=fam_id)#通知进行了副本战斗
    player.model.save()
    return {"result":True,"data":info}



