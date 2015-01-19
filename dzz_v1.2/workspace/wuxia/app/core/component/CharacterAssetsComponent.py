#coding:utf-8
'''
Created on 2014-8-12
角色的资产组件
Copyright 2014 www.9miao.com
'''
import random
from app.configdata import gamedataconfig
from app.core.component.Component import Component
from app.models.equipment import Material

_fall = {
    #((不变的概率集合),(变的概率),其它随机结果)
    2: (set([0.5]), {}, 1),
    3: (set([0.4]), {0.3:1, 0.2:2, 0.1:3}, 3),
    4: (set([0.3]), {0.2:1, 0.15:3, 0.1:4, 0.05:5}, 5)
}

class CharacterAssetsComponent(Component):
    
    def __init__(self, owner):
        """
        @param coin: int角色的铜币（游戏币）
        @param gold: int角色的元宝（人民币）
        @param　energy:　int角色的体力
        """
        Component.__init__(self, owner)
        self.coin = 0
        self.gold = 0
        self.energy = 0
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.coin = self.owner.model.coin
        self.gold = self.owner.model.gold
        self.energy = self.owner.model.energy
        
    def addCoin(self,coin):
        """
        """
        self.coin+=coin
        msg_list = []
        if coin>0:
            msg_list.append("获得%d铜币"%coin)
        else:
            msg_list.append("消耗了%d铜币"%-coin)
        self.owner.addRoleMessage(msg_list)
        self.owner.model.coin = self.coin
        
    def addGold(self,gold):
        """
        """
        self.gold+=gold
        msg_list = []
        if gold>0:
            msg_list.append("获得%d元宝"%gold)
        else:
            msg_list.append("消耗了%d元宝"%-gold)
        self.owner.addRoleMessage(msg_list)

        self.owner.model.gold = self.gold
            
    def addEnergy(self,energy):
        """
        """
        self.energy+=energy
        msg_list = []
        if energy>0:
            msg_list.append("获得%d体力"%energy)
        else:
            msg_list.append("消耗了%d体力"%-energy)
        self.owner.addRoleMessage(msg_list)

        self.owner.model.energy = self.energy

    def addMaterial(self, materials):
        """增加材料(物品)
        @param materials{dict}: {materialId{str}:[count{int},rate]}, {材料ID,材料数量,概率}
        """
        def true_count(key, rate):
            stable, change, default = _fall[key]
            if rate in stable:
                return 0
            else:
                try:
                    interval = change[rate]
                except KeyError:
                    interval = default
                return random.randrange(-interval, interval)


        material_fall = {}
        for mid, _ in materials.iteritems():
            count, rate = _
            if count != 1:
                if 2<=count<=4:
                    key = 2
                elif 5<=count<=10:
                    key = 3
                elif count > 10:
                    key = 4
                count += true_count(key, rate)
            if rate > random.random():
                material_fall[mid] = count

        materials = material_fall

        ms = set()
        for m in self.owner.model.materials:
            if m.materialid in materials:
                m.amount += materials[m.materialid]
                ms.add(m.materialid)
        #没有的材料集合
        needs = set(materials.keys()) - ms
        for materialid in needs:
            self.owner.model.materials.append(Material(materialid=materialid, amount=materials[materialid]))

        msg_list = []
        for mid, mcount in materials.iteritems():
            info = "获得%s个%s" %(mcount, gamedataconfig.ALL_TEMPLATE_INFO[mid]["name"])
            msg_list.append(info)
        self.owner.addRoleMessage(msg_list)
        
    def getReward(self,reward):
        """获取奖励
        """
        coin = reward.get("coin")
        gold = reward.get("gold")
        exp = reward.get("exp")
        material = reward.get("material")
        if coin:
            self.owner.assets.addCoin(coin)
        if gold:
            self.owner.assets.addGold(gold)
        if exp:
            self.owner.level.addExp(exp)
        if material:
            self.addMaterial(material)
        
        
        
        
        