#coding:utf-8
'''
Created on 2014-8-12

Copyright 2014 www.9miao.com
'''
from mongoengine.queryset import DoesNotExist
from app.configdata import msgconfig
from app.handler.service import serviceHandle
from app.models.role import Role
from app.core.charater import Charater


@serviceHandle("gongfa")
def gongfa(openid, request):
    """功法
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = []
    info = ["%s.%s" % (i, partner.getName()) for i, partner in enumerate(player.partners.getPartners(),start=1)]
    info.append("\n提示：输入名字前序号提高功法，例如1")
    player.model.prev_command = "gongfa"
    player.model.save()
    player.plot.notice("gongfa")
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("gongfa_enter")
def gongfa_enter(openid, request):
    """
    """
    try:
        seqno = int(request)
    except ValueError:
        return {"result":False,"data":"伙伴序号有误，请重新选择"}
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    try:
        partner = player.partners.getPartnerBySeqno(seqno)
    except IndexError:
        return {"result":False,"data":"伙伴序号有误，请重新选择"}
    info = partner.gongfa.enter_info()
    player.model.prev_command = "gongfa_enter"
    player.model.prev_objectid = seqno
    player.model.save()
    return {"result":True,"data":info}


@serviceHandle("gongfa_choice")
def gongfa_choice(openid, request):
    """具体功法选择
    """
    try:
        no = int(request)
    except ValueError:
        return {"result":False,"data":"提升功法序号有误，请重新选择"} 
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = player.model.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)
    success, info = partner.gongfa.choice(no)
    player.model.prev_command = "gongfa_choice"
    player.model.prev_objectid2 = no
    if success:
        player.model.save()
    return {"result":True,"data":info}


@serviceHandle("gongfa_practice")
def gongfa_practice(openid, request):
    """功法修炼
    """
    try:
        no = int(request)
    except ValueError:
        return {"result":False,"data":"序号有误，请重新选择"}
    if no not in [1,2]:
        return {"result":False,"data":"序号有误，请重新选择"}
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = player.model.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)
    gfno = player.model.prev_objectid2
    success, info = partner.gongfa.practice(gfno,no)
    if success:
        player.model.save()
        partner.gongfa.save()
    return {"result":True,"data":info}


