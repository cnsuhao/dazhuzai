#coding:utf8
'''
Created on 2014-6-23

Copyright 2014 www.9miao.com
'''
from app.handler.service import serviceHandle
from app.models.role import Role
from app.core.battle import DoFightWithMonster
from app.core.charater import Charater
import random

@serviceHandle("fight")
def fight(openid,request):
    """获取当前地图信息
    """
    from app.configdata import gamedataconfig
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    #如果是剧情战斗
    if player.plot.IsPlotFight():
        battleid = player.plot.getPlotBattleId()
        battle_info = gamedataconfig.ALL_FIGHT_INFO.get(battleid)
        m_config_str = battle_info.get("monster")
        
        #战斗描述
        fight_desc = battle_info.get("desc")
        fight = DoFightWithMonster(player, m_config_str)
        fight.start()
#         player.addRoleMessage(fight.rounds)
        player.plot.notice("fight")
        info = fight_desc+"\n"+"\n".join(fight.rounds)
    else:
        info = "没有战斗对象"
    player.model.save()
    return {"result":True,"data":info}



    
    