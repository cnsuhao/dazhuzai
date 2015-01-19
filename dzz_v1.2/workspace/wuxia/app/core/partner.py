#coding:utf-8
'''
Created on 2014-8-12
伙伴
Copyright 2014 www.9miao.com
'''
from app.core.component.CharacterAttributeComponent import CharacterAttributeComponent
from app.core.component.CharaterEquipmentComponent import CharacterEquipmentComponent
from app.core.component.CharacterRoadComponent import CharacterRoadComponent
from app.core.component.CharacterGongfaComponent import CharacterGongfaComponent

class Partner:
    
    def __init__(self,partner_id,owner):
        """
        @param partner_id: 伙伴的ID
        @param owner: character 伙伴的归属者
        """
        self.partner_id =partner_id
        self.template = int(partner_id.split(":")[-1])
        self.owner = owner
        self.level = self.owner.level.level
        self.exp = self.owner.level.exp
        self.coin = self.owner.assets.coin
        self.gold = self.owner.assets.gold
        self.attribute = CharacterAttributeComponent(self)
        self.equipment =  CharacterEquipmentComponent(self)
        self.road = CharacterRoadComponent(self)
        self.gongfa = CharacterGongfaComponent(self)
    
    def getName(self):
        """获取伙伴的名称
        """
        return self.attribute.getName()
        
    def formatPartnerInfo(self):
        """格式化伙伴信息
        """
        pass
        
    def getBattleAttribut(self):
        """获取战斗属性
        """
        info = self.attribute.getAttribute()
        info["name"] = self.getName()
        info["hp"] = info["maxhp"]
        info["died"] = 0
        skills = self.attribute.getSkills()
        info.update(skills)
        return info
    
    @property
    def formationSerial(self):
        return self.attribute.getFormationSerial()
        
    

    