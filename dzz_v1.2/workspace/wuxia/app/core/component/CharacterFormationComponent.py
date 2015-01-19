#coding:utf-8
'''
Created on 2014-8-14
角色阵型信息
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component
from app.configdata.gamedataconfig import LEAD_PROFESSION,MAX_MEMBER


class CharacterFormationComponent(Component):
    """角色阵型信息
    """
    
    def __init__(self, owner):
        Component.__init__(self, owner)
        self.initFormation()
        
    def initFormation(self):
        """
        """
        if not self.owner.model.formation:
            from app.models.role import Formation
            self.owner.model.formation = Formation()
        if not self.checkLeadInFormation():
            self.setFormation(1, LEAD_PROFESSION)
            
        
    def checkLeadInFormation(self):
        """检测主角是否在阵法中
        """
        for _p in range(1,MAX_MEMBER+1):
            if str(LEAD_PROFESSION)==str(getattr(self.owner.model.formation,"position_%d"%_p)):
                return True
        return False
        
    def getFormationInfo(self):
        """获取阵型信息
        """
        formation_list = []
        for _p in range(1,MAX_MEMBER+1):
            partner_id = getattr(self.owner.model.formation,"position_%d"%_p)
            if not partner_id:
                info = "位置%d:【无】\n"%(_p)
            else:
                partner = self.owner.partners.getPartnerById(partner_id)
                info = "位置%d:【%s】\n"%(_p,partner.getName())
            formation_list.append(info)
        return "".join(formation_list)
    
    def getBattleFormation(self):
        """获取战斗阵型
        """
        formation_info = {}
        for _p in range(1,MAX_MEMBER+1):
            partner_id = getattr(self.owner.model.formation,"position_%d"%_p)
            if not partner_id:
                continue
            else:
                partner = self.owner.partners.getPartnerById(partner_id)
                formation_info[_p] = partner
        return formation_info
        
    def setFormation(self,position,partner_id):
        """设置阵法
        """
        setattr(self.owner.model.formation, "position_%d"%position, partner_id)

    def reset(self):
        """重置阵法
        """
        self.setFormation(1, LEAD_PROFESSION)
        for _p in range(2,MAX_MEMBER+1):
            self.setFormation(_p, 0)

        
        