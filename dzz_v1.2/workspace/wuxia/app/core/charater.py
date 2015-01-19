#coding:utf-8
'''
Created on 2014-7-22

Copyright 2014 www.9miao.com
'''
from app.core.component.CharaterLevelComponent import CharacterLevelComponent
from app.core.component.CharaterPlotComponent import CharacterPlotComponent
from app.core.component.CharacterPositionComponent import CharacterPositionComponent
# from app.core.component.CharacterAttributeComponent import CharacterAttributeComponent
# from app.core.component.CharaterEquipmentComponent import CharacterEquipmentComponent
from app.core.component.CharacterFamComponent import CharacterFamComponent
from app.core.component.CharacterAssetsComponent import CharacterAssetsComponent
from app.core.component.CharacterPartnersComponent import CharacterPartnersComponent
from app.core.component.CharacterFormationComponent import CharacterFormationComponent
from app.core.component.CharacterArenaComponent import CharacterArenaComponent
from app.core.component.CharacterSignComponent import CharacterSignComponent
from app.core.component.CharacterPackageComponent import CharacterPackageComponent

class Charater:
    """角色类
    """
    def __init__(self,rolemodel):
        """
        @param rolemodel: 角色的数据模型
        @param plot: 角色的剧情信息
        @param postion: 角色的配置信息
        @param attribute: 角色的属性信息
        @param level: 角色的等级信息
        @param assets: 角色的资产
        @param fam: 角色的秘境记录
        @param equipment: 角色的装备组件
        """
        self.model = rolemodel
        self.openid = self.model.openid
        self.plot = CharacterPlotComponent(self)
        self.postion = CharacterPositionComponent(self)
#         self.attribute = CharacterAttributeComponent(self)
        self.level = CharacterLevelComponent(self)
        self.assets = CharacterAssetsComponent(self)
        self.fam = CharacterFamComponent(self)
        self.partners = CharacterPartnersComponent(self)
        self.formation = CharacterFormationComponent(self)
#        self.equipment = CharacterEquipmentComponent(self)
        self.arena = CharacterArenaComponent(self)
        self.sign = CharacterSignComponent(self)
        self.package = CharacterPackageComponent(self)
        
    def addRoleMessage(self,msg_list):
        """添加消息
        """
        self.model.message.extend(msg_list)
    
    def getBattleAttribut(self):
        """获取战斗属性
        """
        info = {"name":self.model.nickname,
            "hp":200,
            "level":self.level.level,
            "force":10,
            "physique":10,
            "iforce":10,
            "dodge":10,
            "skills":[],
            "speed":(self.level.level*0.1+1)*10}
        return info
    

        