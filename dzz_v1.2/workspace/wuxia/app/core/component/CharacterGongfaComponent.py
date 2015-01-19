#coding:utf-8
'''
Created on 2014-7-22
角色属性组件
Copyright 2014 www.9miao.com
'''
import random
import math
from collections import OrderedDict
from mongoengine.queryset import DoesNotExist
from app.core.component.Component import Component
from app.models.partner import Partner
from app.configdata import gamedataconfig

_GONGFA = ("maxhp", "hit", "dodge", "crit", "tenacity")
_GONGFA_NAME = ("气血", "命中", "闪躲", "暴击", "韧性")
_PRACTISE = ("领悟", "突破")

class CharacterGongfaComponent(Component):
    
    def __init__(self,owner):
        """
        """
        Component.__init__(self, owner)
        self.powner = self.owner.owner
        self.initData()

    def initData(self):
        """和灵路使用同一个数据模型
        """
        self.partnerModel = self.owner.road.partnerModel


    def save(self):
        self.partnerModel.save()

    def __getattr__(self, name):
        """同时返回领悟和突破等级
        """
        return (self.partnerModel[name+'_comprehend'], self.partnerModel[name+'_break'])

    def addition(self, name):
        """获取属性加成
        """
        level_1,level_2 = getattr(self, name)
        return int(gamedataconfig.ALL_GONGFA_GROW[name]*level_1*gamedataconfig.ALL_GONGFA_BREAK[level_2]["ratio"])

    def enter_info(self):
        info = []
        for i,k in enumerate(_GONGFA,start=1):
            level = getattr(self, k)
            info.append("%s.%s：领悟%s级，突破%s级，加成属性%s" %(i, _GONGFA_NAME[i-1], level[0], level[1], self.addition(k)))
        info.append("\n领悟消耗[玉灵果]，突破消耗[天灵莲]，请输入需要提升的功法的序号")
        return "\n".join(info)

    def comprehend_consume(self, gf):
        """何种功法领悟消耗
        """
        level = getattr(self, gf)[0]
        if level <= 10:
            return 1
        else:
            return math.ceil(float(level-7)/2)

    def break_consume(self, gf):
        """何种功法突破消耗
        """
        level = getattr(self, gf)[1]
        return gamedataconfig.ALL_GONGFA_BREAK[level]["need"]

    def getBattleAttribute(self):
        """获取战斗属性
        """
        return dict(((k,self.addition(k)) for k in _GONGFA))

    def choice(self, no):
        """选择具体功法
        """
        try:
            gf = _GONGFA[no-1]
        except IndexError:
            return False, "提升功法序号有误，请重新选择"
        #80200001
        comprehend_mid = gamedataconfig.ALL_GONGFA_GROW["comprehend_mid"]
        break_mid = gamedataconfig.ALL_GONGFA_GROW["break_mid"]
        c_1, c_2 = self.powner.package.get_count(comprehend_mid, break_mid)
        n_1, n_2 = self.powner.package.get_name(comprehend_mid, break_mid)
        info = []
        info.append("当前拥有[%s] %s，[%s] %s" %(n_1, c_1, n_2, c_2))
        info.append("1. 领悟：本次领悟消耗%s%s" %(self.comprehend_consume(gf), n_1))
        info.append("2. 突破：本次突破消耗%s%s" %(self.break_consume(gf), n_2))
        info.append("\n提示：请选择功能：")
        return True, "\n".join(info)

    def practice(self, gfno, no):
        """修炼
        """
        gf = _GONGFA[gfno-1]
        levels = getattr(self, gf)
        if no == 1: #领悟
            mid = gamedataconfig.ALL_GONGFA_GROW["comprehend_mid"]
            need = self.comprehend_consume(gf)
            level = levels[0]
            maxlevel = -1
            name = "_comprehend"
        else: #突破
            mid = gamedataconfig.ALL_GONGFA_GROW["break_mid"]
            need = self.break_consume(gf)
            level = levels[1]
            maxlevel = 10
            name = "_break"

        count = self.powner.package.get_count(mid)[0]
        success, plevel,hint = False, self.powner.model.level,_PRACTISE[no-1]
        if plevel <= level:
            info = "%s失败，等级不足" % hint
        elif maxlevel != -1 and level >= maxlevel:
            info = "%s失败，已达到最高级" % hint
        elif need > count:
            info = "%s失败，材料不足" % hint
        else:
            success = True
            self.powner.package.update_count({mid:-need})
            self.partnerModel[gf+name] += 1
            info = "[%s]%s成功，加成属性%s" % (_GONGFA_NAME[gfno-1], hint, self.addition(gf))
            info += "\n\n提升：输入1继续领悟，输入2继续突破"

        return success, info













        
        
    
     
    
    
    
    
    