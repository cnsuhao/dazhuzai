#coding:utf-8
'''
Created on 2014-8-14
角色的伙伴组件
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component
from app.core.partner import Partner
from app.configdata.gamedataconfig import LEAD_PROFESSION

class CharacterPartnersComponent(Component):
    """用来记录角色的宠物信息
    """
    
    def __init__(self, owner):
        Component.__init__(self, owner)
        self.initLead()
        
    def initLead(self):
        """初始化主角
        """
        lead_profession = LEAD_PROFESSION
        self.AddPartner(lead_profession)
        
    def AddPartner(self,partner):
        """添加一个伙伴
        @param partner: int　伙伴的模板ID
        """
        if self.checkHasPartner(partner):
            return False
        self.owner.model.partners.append(partner)
        return True
        
    def getLeadPartnerId(self):
        """按照　openid:profession 的规则来生成伙伴的唯一ID
        """
        lead_profession = LEAD_PROFESSION
        return self.owner.openid+":"+str(lead_profession)
    
    def getPartnerById(self,partner_id):
        """根据角色的伙伴ID获取伙伴实例
        """
        last_partner_id = self.owner.openid+":"+str(partner_id)
        partner = Partner(last_partner_id, self.owner)
        return partner

    def getPartnerBySeqno(self,seqno):
        """根据partners的序号创建伙伴实例
        """
        partner_id = self.owner.openid+":"+str(self.owner.model.partners[seqno-1])
        return Partner(partner_id, self.owner)
    
    def getPartnerIdList(self):
        """按照　openid:profession 的规则来生成伙伴的唯一ID
        """
        openid = self.owner.openid
        return [openid+":"+str(profession) for profession in self.owner.model.partners]

    def getPartnerCount(self):
        """获取partner总数
        """
        return len(self.owner.model.partners)

    def getPartners(self):
        """获取所有伙伴实例
        """
        openid = self.owner.openid
        return [Partner(openid+":"+str(profession),self.owner) for profession in self.owner.model.partners]

    
    def checkHasPartner(self,partner):
        """检测是否以及拥有指定的伙伴
        @param partner: int　伙伴的模板ID
        """
        return partner in self.owner.model.partners
        
    def getLeadInfo(self):
        """获取主角伙伴的信息
        """
        partner_id = self.getLeadPartnerId()
        lead = Partner(partner_id, self.owner)
        return lead.attribute.getAttributeFormat()

    def getLeadCombat(self):
        partner_id = self.getLeadPartnerId()
        lead = Partner(partner_id, self.owner)
        return lead.attribute.getCombat()
        
    def getPartnersInfo(self):
        """获取所有伙伴的信息
        """
        pass
    

    
    
    
        
        