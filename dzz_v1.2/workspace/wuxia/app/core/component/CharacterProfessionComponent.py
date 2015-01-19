#coding:utf-8
'''
Created on 2014-8-7
角色职业组件
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component

class CharacterProfessionComponent(Component):
    
    def __init__(self, owner):
        Component.__init__(self, owner)
        self.profession = 0
        
    def initData(self):
        """初始化职业数据
        """
        self.profession = self.owner.model.profession
        
    def getProfession(self):
        """获取角色的职业
        """
        return self.profession
        
    def getProfessionName(self):
        """获取职业名称
        """
        
        
        
        