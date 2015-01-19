#coding:utf-8
'''
Created on 2014-7-22
角色属性组件
Copyright 2014 www.9miao.com
'''
import random
import operator
from datetime import datetime
from mongoengine.queryset import DoesNotExist
from app.core.component.Component import Component
from app.models.partner import Partner
from app.configdata import gamedataconfig
from app.core.battle import DoFightPartnerWithMonster

ROADS = gamedataconfig.ALL_ROAD_CONFIG

_DEFAULT_ENERGY = 8
_BEGIN_LOAD = "1"
_REWARDS = {
    "explode": "普通破防",
    "magic_explode": "法术破防",
    "fatal": "致命",
    "speed": "速度"
}

class CharacterRoadComponent(Component):
    
    def __init__(self,owner):
        """
        """
        Component.__init__(self, owner)
        self.powner = self.owner.owner
        self.initData()

    def initData(self):
        try:
            self.partnerModel = Partner.objects.get(partner_id=self.owner.partner_id)
        except DoesNotExist:
            self.partnerModel = Partner(partner_id=self.owner.partner_id, roadnode=_BEGIN_LOAD)
            self.save()
        now = datetime.now()
        add_time = self.powner.model.energy_add_time
        if add_time is None or (now.date()- add_time.date()).days != 0: #不是同一天
            self.powner.model.energy = _DEFAULT_ENERGY
        else:
            hours = (now - add_time).seconds / 3600
            if self.powner.model.energy < 8 and hours > 0:
                self.powner.model.energy += hours

        self.powner.model.energy_add_time = now


    def save(self):
        if self.partnerModel is not None:
            self.partnerModel.save()

    def __getattr__(self, name):
        return getattr(self.partnerModel, name)

    @property
    def energy(self):
        """获取当前体力
        """
        return self.powner.model.energy

    @property
    def current(self):
        """当前境界
        """
        return ROADS[self.roadnode]["node_name"]

    def next_info(self):
        """下一境界信息
        """
        next = ROADS[ROADS[self.roadnode]["next_node"]]
        return next["node_name"], next["xiuwei"]

    def enter_info(self):
        info = []
        info.append("当前境界[%s]，" % self.current)
        try:
            next_name, next_wiuwei = self.next_info()
            info.append("距离下一境界[%s]，还需%s修为" %(next_name,max(next_wiuwei-self.xiuwei,0)))
        except KeyError:
            info.append("已达灵路尽头...")
        return "".join(info)

    def update_node(self, next_node):
        """更新当前节点
        """
        self.partnerModel.roadnode = next_node

    def rewrad(self, reward):
        """获得奖励
        """
        if not reward:
            return ''
        reward = eval(reward)
        info = []
        for k,v in reward.items():
            if k in _REWARDS:
                _v = getattr(self.partnerModel, k)
                setattr(self.partnerModel, k, v+_v)
                info.append("%s+%s" %(_REWARDS[k],v))
        return "\n".join(info)

    def explore(self):
        """灵路探险
        """
        try:
            next_name, next_wiuwei = self.next_info()
        except KeyError:
            return "探险通关，已达灵路尽头..."
        xiuwei = reduce(operator.mul,random.sample(range(2,7),4)) * self.powner.model.level

        now = ROADS[self.roadnode]
        info = []
        if not self.prev_failed:
            info.append("经过一路探险，获得%s修为，获得了%s经验值" %(xiuwei, now["common_reward"] or 0))
            self.partnerModel.xiuwei += xiuwei
        if self.xiuwei >= next_wiuwei:
            info.append("已经触摸到[%s]，开始突破战斗" % next_name)
            battleid = now["battleid"]
            battle_info = gamedataconfig.ALL_FIGHT_INFO.get(battleid)
            m_config_str = battle_info.get("monster")
            fight = DoFightPartnerWithMonster(self.owner, m_config_str)
            fight.start()
            info.append("\n".join(fight.rounds))
            if fight.result:
                self.update_node(now["next_node"])
                info.append("恭喜你突破成功,%s" % self.enter_info())
                self.partnerModel.prev_failed = False
                info.append(self.rewrad(now["node_reward"]))
            else:
                info.append("突破失败，太遗憾了 ，当前境界[%s]，继续探险可再次突破" % self.current)
                self.partnerModel.prev_failed = True
        self.powner.model.energy -= 1
        self.save()
        return "\n".join(info)

    def getBattleAttribute(self):
        """获取战斗属性
        """
        return dict(((k,self.partnerModel[k]) for k in _REWARDS))







        
        
    
     
    
    
    
    
    