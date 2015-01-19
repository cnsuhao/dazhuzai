#coding:utf8
'''
Created on 2014-9-3

Copyright 2014 www.9miao.com
'''

from app.handler.service import serviceHandle
from app.models.role import Role
from app.core.charater import Charater
from app.core.component.CharacterSignComponent import EXCHANGE_LIST
from app.configdata import gamedataconfig
from app.utils.hashtools import getDigest

@serviceHandle('sign')
def sign(openid, request):
    """签到
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.sign.sign()
    player.model.save()
    player.plot.notice("sign")
    return {"result":True,"data":info}

@serviceHandle("exchange_info")
def exchange_info(openid, request):
    """积分兑换信息
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.sign.exchange_info()
    player.model.prev_command = "exchange_info"
    player.model.save()
    player.plot.notice("exchange_info")
    return {"result":True,"data":info}

@serviceHandle("exchange")
def exchange(openid, request):
    """积分兑换
    """
    failed = False
    try:
        seqno, num = map(int, request.split('@'))
    except:
        failed = True
    if failed or seqno not in EXCHANGE_LIST:
        return  {"result":True,"data":"输入的序号有误，请重新输入，输入物品序号+“@”+兑换数量即可兑换相应物品，例输入“1@2”可兑换2个元宝"}
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    success, info = player.sign.exchange(seqno, num)
    if success:
        player.model.save()
    return {"result":True,"data":info}

@serviceHandle("rob_info")
def rob_info(openid, request): 
    """打劫信息
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.sign.rob_info()
    player.model.prev_command = "rob_info"
    player.model.save()
    return {"result":True,"data":info}


@serviceHandle("rob")
def rob(openid, request):
    """打劫
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    help = "\n提示：输入玩家序号可以继续打劫"
    if player.sign.rob_time <= 0:
        return {"result":True,"data":"您今天做的坏事已经够多了，不要再打劫别人啦！"}
    try:
        ropenid = player.sign.rob_user[int(request)-1]
    except (IndexError, ValueError):
        return {"result":True,"data":"序号选择有误，请重新选择"}
    robed_player = Charater(Role.objects.get(openid=ropenid))
    if robed_player.sign.robed_time >= 10:
        info = "他今天被打劫的次数已经够多了，不要再打劫他啦！！"
    else:
        info = player.sign.rob(robed_player)
        robed_player.model.save()
    player.addRoleMessage([player.sign.rob_info()])
    player.model.save()
    return {"result":True,"data":info}




 