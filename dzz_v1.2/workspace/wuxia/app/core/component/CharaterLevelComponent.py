#coding:utf-8
'''
Created on 2014-7-22
角色的等级组件
Copyright 2014 www.9miao.com
'''

from app.core.component.Component import Component
from app.configdata import gamedataconfig

class CharacterLevelComponent(Component):
    
    def __init__(self,owner):
        """初始化
        """
        Component.__init__(self, owner)
        self.level = 1
        self.exp = 0
        self.coppercash = 0
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.level = self.owner.model.level
        self.exp = self.owner.model.exp
        
    def getMaxExp(self):
        """获取当前等级的最大经营者
        """
        expinfo = gamedataconfig.EXPERIENCE_CONFIG.get(self.level,{})
        return expinfo.get("maxexp",100000000)
    
    def addExp(self,exp):
        """添加经验值
        """
        self.exp+=exp
        msg_list = []
        msg_list.append("获得%d经验"%exp)
        while self.exp>=self.getMaxExp():
            preexp = self.getMaxExp()
            self.level+=1
            msg_list.append("等级提升到Lv%d"%self.level)
            #self.exp=self.exp-self.getMaxExp()
            self.exp = self.exp - preexp
        self.owner.addRoleMessage(msg_list)

        self.owner.model.level = self.level
        self.owner.model.exp = self.exp


        