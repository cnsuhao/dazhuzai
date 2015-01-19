#coding:utf8
'''
Created on 2014-7-29

Copyright 2014 www.9miao.com
'''
from itertools import izip
from collections import OrderedDict
from mongoengine.queryset import DoesNotExist
from app.configdata import msgconfig
from app.configdata.gamedataconfig import ALL_PARTNER_INFO, LEAD_PROFESSION
from app.handler.service import serviceHandle, wservice
from app.models.role import Role
from app.models.equipment import Equipment
from app.core.charater import Charater
from app.core.component.CharaterEquipmentComponent import equip_type, EQUIPMENT_KEY, EQUIPMENT
                                                        


@serviceHandle('equipchoice')
def equipchoice(openid, request):
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = []
    info.append("请选择操作对象：")
    for i, partner in enumerate(player.partners.getPartners(),start=1):
        info.append("%s.%s" % (i, partner.getName()))
    info.append("\n操作提示：输入名字前序号，可以查看相应人物装备信息，例如：输入“1”获得主角装备信息")
    weiuser.prev_command = "equipchoice"
    weiuser.save()
    return {"result":True,"data":"\n".join(info)}


@serviceHandle('equipment')
def equipment(openid, request):
    """查看装备
    """
    if not request.isdigit():
        return {"result":True,"data":"操作对象序号有误"}
    seqno = int(request)
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    if seqno < 1 or seqno > player.partners.getPartnerCount():
        return {"result":True,"data":"操作对象序号有误"}

    partner = player.partners.getPartnerBySeqno(seqno)
    weiuser.prev_objectid = seqno
    weiuser.prev_command = "equipment"
    weiuser.save()
    info = partner.equipment.view()
    return {"result":True,"data":info}

def get_equipmodel(openid, weiuser):
    """获取装备模型
    """
    pno = weiuser.prev_objectid
    partnerid = LEAD_PROFESSION if pno == 1 else weiuser.partners[pno-2]
    pid = partnerId(openid, partnerid)
    equipment = Equipment.objects.get(openid=pid)
    return equipment


@serviceHandle("advance")
def advance(openid,request):
    """装备进阶
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = weiuser.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)
    equipment_key = equip_type(request)
    if equipment_key is None:
        info = partner.equipment.advanceView()
    else:
        print equipment_key
        partner.equipment.updateEquipType(equipment_key)
        if partner.equipment.isTopAdvance():
            info = "无法进阶  已经是最高级"
        else:
            flag, info = partner.equipment.advance()
            player.plot.notice("advance") #通知进阶
            if flag:
                player.model.save()
                partner.equipment.equip_model.save()
            
    return {"result":True,"data":info}


@serviceHandle("update")
def update(openid, request):
    """装备升品
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = weiuser.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)
    equipment_key = equip_type(request)
    if equipment_key is None:
        info = partner.equipment.updateView()
    else:
        print equipment_key
        partner.equipment.updateEquipType(equipment_key)
        if partner.equipment.isTopUpdate():
            info = "无法升品  已经是最高级"
        else:
            flag, info = partner.equipment.update()
            player.plot.notice("update") #通知升品
            if flag:
                player.model.save()
                partner.equipment.equip_model.save()
                
    return {"result":True,"data":info}


@serviceHandle('strengthen')
def strengthen(openid, request):
    """装备强化
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = weiuser.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)
    equipment_key = equip_type(request)
    if equipment_key is None:
        info = partner.equipment.strengthenView()
    else:
        partner.equipment.updateEquipType(equipment_key)
        print partner.equipment.getBattleAttribute()
        if partner.equipment.isTopStren():
            info = "无法强化 已经是最高级"
        else:
            if not partner.equipment.strenRoleLevelEnough():
                info = "当前人物等级不够"
            elif not partner.equipment.moneyEnough():
                info = "强化失败 铜钱不足"
            else:
                info = partner.equipment.strengthen()
                player.plot.notice("strengthen") #通知强化
                player.model.save()
                partner.equipment.equip_model.save()
    return {"result":True,"data":info}

@serviceHandle('autostrengthen')
def autostrengthen(openid, request):
    """自动强化
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    seqno = weiuser.prev_objectid
    partner = player.partners.getPartnerBySeqno(seqno)

    flags = dict(izip(EQUIPMENT_KEY,(False,)*3))
    success = OrderedDict(izip(EQUIPMENT_KEY,(None,)*3))
    minus = set()
    for i in xrange(5):
        for key in EQUIPMENT_KEY:
            if key in minus:
                continue
            partner.equipment.updateEquipType(key)
            if partner.equipment.isTopStren():
                minus.add(key)
                flags[key] = 1
            elif not partner.equipment.strenRoleLevelEnough():
                minus.add(key)
                flags[key] = 2
            elif not partner.equipment.moneyEnough():
                minus.add(key)
                flags[key] = 3
            else:
                success[key] = partner.equipment.strengthen() + '\n'
    info = [v for v in success.itervalues() if v]
    if info: #至少有一件强化成功
        player.model.save()
        partner.equipment.equip_model.save()
    else:
        c = {
            1: "无法强化 已经是最高级",
            2: "强化失败 当前人物等级不够",
            3: "强化失败 铜钱不足"
        }
        values = set(flags.itervalues())
        if len(values) == 1: #强化失败原因都相同
            info.append(c[values.pop()])
        else:
            for key in EQUIPMENT_KEY:
                info.append("%s %s" %(EQUIPMENT[key], c[flags[key]]))
    player.plot.notice("strengthen") #通知强化
    player.model.save()
    info = "\n".join(info)
    return {"result":True,"data":info}





    
    