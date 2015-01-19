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

_ENERGY_FULL = 8

@serviceHandle("road")
def road(openid, request):
    """灵路
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = []
    info = ["%s.[%s]%s" % (i, partner.getName(), partner.road.enter_info()) for i, partner in enumerate(player.partners.getPartners(),start=1)]
    info.append("当前体力%s（每1小时恢复1点）" %player.model.energy)
    info.append("\n提示：输入名字前序号进行灵路探险，例如1")
    player.model.prev_command = "road"
    player.model.save()
    player.plot.notice("enter_road")
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("road_explore")
def explore(openid, request):
    """灵路探险
    """
    try:
        seqno = int(request)
    except ValueError:
        return {"result":True,"data":"伙伴序号有误，请重新选择"}
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    try:
        partner = player.partners.getPartnerBySeqno(seqno)
    except IndexError:
        return {"result":True,"data":"伙伴序号有误，请重新选择"}
    if partner.road.energy <= 0:
        info = "当前体力不足，每1小时恢复1点\n提示；每天可以购买20次体力，当前购买体力需要消耗%s元宝，输入“购买体力”可购买体力" % 2*player.model.energy_buytime
    else:
        info = partner.road.explore()
        player.plot.notice("explore")
        msg = ["%s.[%s]%s" % (i, partner.getName(), partner.road.enter_info()) for i, partner in enumerate(player.partners.getPartners(),start=1)]
        msg.append("当前体力%s（每1小时恢复1点）" %player.model.energy)
        msg.append("\n提示：输入名字前序号将进行灵路探险，例如1")
        player.addRoleMessage(["\n".join(msg)])
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle("buy_energy")
def buy(openid, request):
    """购买体力
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    cost = player.model.energy_buytime*2
    if player.model.energy_buytime > 20:
        info = "同学今日购买次数已达上限，明天再来吧"
    elif player.model.gold >= cost:
        player.model.gold -= cost
        player.model.energy_buytime += 1
        player.model.energy += 1
        player.model.save()
        info = "购买成功，消耗%s元宝，当前体力%s" %(cost, player.model.energy)
    else:
        info = "购买失败，元宝不足"
    return {"result":True,"data":info}



