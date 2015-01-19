#coding:utf-8
'''
Created on 2014-7-22
角色属性组件
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component
from app.configdata import gamedataconfig


class CharacterAttributeComponent(Component):
    
    def __init__(self,owner):
        """
        """
        Component.__init__(self, owner)
        
    def getName(self):
        """获取伙伴的名称
        """
        init_attr = gamedataconfig.ALL_PARTNER_INFO.get(self.owner.template,{})
        return init_attr.get("partner_name","未知")
        
    def getAttribute(self):
        """获取角色的属性
        """
        init_attr = gamedataconfig.ALL_PARTNER_INFO.get(self.owner.template,{})#获取角色的基础属性
        equip_attr = self.owner.equipment.getBattleAttribute()#获取角色的装备属性
        skill_attr = {}#角色的被动技能属性
        road_atttr = self.owner.road.getBattleAttribute() #伙伴灵路附加属性
        gongfa_attr = self.owner.gongfa.getBattleAttribute() #功法附加属性
        level = self.owner.level
        info = {}
        info["level"] = level
        info['maxhp'] = int((init_attr.get("maxhp",0)+(100+level)*init_attr.get("hp_grow",0)+equip_attr.get("maxhp",0)+gongfa_attr.get("maxhp",0))*(1+skill_attr.get("maxhp",0)))#血量
        info['attack'] = int((init_attr.get("attack",0)+(100+level)*init_attr.get("attack_grow",0)+equip_attr.get("attack",0))*(1+skill_attr.get("attack",0)))#普通攻击
        info['magic_attack'] = int((init_attr.get("magic_attack",0)+(100+level)*init_attr.get("magic_attack_grow",0)+equip_attr.get("magic_attack",0))*(1+skill_attr.get("magic_attack",0))) #内力攻击
        info['defend'] = int((init_attr.get("defend",0)+(100+level)*init_attr.get("defend_grow",0)+equip_attr.get("defend",0)+road_atttr.get("defend",0))*(1+skill_attr.get("defend",0)))  #普通防御
        info['magic_defend'] = int((init_attr.get("magic_defend",0)+(100+level)*init_attr.get("magic_defend_grow",0)+equip_attr.get("magic_defend",0))*(1+skill_attr.get("magic_defend",0)))
        info['explode'] = int((init_attr.get("explode",0)+(100+level)*init_attr.get('explode_grow',0)+road_atttr.get("explode",0))*(1+skill_attr.get('explode',0)))
        info['magic_explode'] = int((init_attr.get("magic_explode",0)+(100+level)*init_attr.get('magic_explode_grow',0)+road_atttr.get("magic_explode",0))*(1+skill_attr.get('magic_explode',0)))
        info['hit'] = int((init_attr.get("hit",0)+init_attr.get('hit_grow',0)*level+gongfa_attr.get("hit",0))*(1+skill_attr.get('hit',0))) #命中
        info['dodge'] = int((init_attr.get("dodge",0)+init_attr.get('dodge_grow',0)*level+gongfa_attr.get("dodge",0))*(1+skill_attr.get('dodge',0))) #闪避
        info['crit'] = int((init_attr.get("crit",0)+init_attr.get('crit_grow',0)*level+gongfa_attr.get("crit",0))*(1+skill_attr.get('crit',0))) #暴击
        info['tenacity'] = int((init_attr.get("tenacity",0)+init_attr.get('tenacity_grow',0)*level+gongfa_attr.get("tenacity",0))*(1+skill_attr.get('tenacity',0)))#韧性
        info['deadly'] = (init_attr.get("fatal",0)+road_atttr.get("fatal",0))*(1+skill_attr.get('deadly',0)) #致命
        info['speed'] = (init_attr.get("speed",0)+road_atttr.get("speed",0)+init_attr.get('speed_grow',0)*level)*(1+skill_attr.get('tenacity',0)) #速度
        info["hp"] = info['maxhp']
        info['dander'] = 0 #怒气
        return info
    
    def getSkills(self):
        """获取角色的技能
        """
        partner_info = gamedataconfig.ALL_PARTNER_INFO.get(self.owner.template,{})
        info = {}
        info["ord_skill"] = partner_info.get("ordinary_skill","90000")
        info["skill_1"] = partner_info.get("skill_1","90000")
        info["skill_2"] = partner_info.get("skill_2","90000")
        skill_cd = gamedataconfig.ALL_SKILL_INFO.get(info["skill_2"])["cd"]
        info["skill_cd"] = {"skill_2":skill_cd}
        return info

    def getSkillDetails(self):
        skillinfo = self.getSkills()
        skill_1 = skillinfo["skill_1"]
        skill_2 = skillinfo["skill_2"]
        attr = {}
        attr["skill_1"] = gamedataconfig.ALL_SKILL_INFO.get(skill_1)["skill_name"]
        attr["skill_1_desc"] = gamedataconfig.ALL_SKILL_INFO.get(skill_1)["skill_desc"]
        attr["skill_2"] = gamedataconfig.ALL_SKILL_INFO.get(skill_2)["skill_name"]
        attr["skill_2_desc"] = gamedataconfig.ALL_SKILL_INFO.get(skill_2)["skill_desc"]
        return attr        
        
    def getCombat(self, info=None):
        """获取战斗力
        """
        if info is None:
            info = self.getAttribute()
        #return sum(info.values())
        return int(((info["attack"]+float(info["magic_attack"])/3)*0.5+(info["explode"]+float(info["magic_explode"])/2)*1+ \
                    (info["magic_defend"]+float(info["defend"])/2)*0.4+info["maxhp"]*0.2+ \
                    (info['crit']+info['tenacity']+info['hit'])*2)*pow(1.01, info["level"]-1)
                )
    
    def getAttributeFormat(self):
        """获取角色属性说明
        """
        attr = self.getAttribute()
        #combat = sum(attr.values())
        combat = self.getCombat(attr)
        skillinfo = self.getSkills()
        skill_1 = skillinfo["skill_1"]
        skill_2 = skillinfo["skill_2"]
        attr["name"] = self.getName()
        attr["level"] = self.owner.level
        attr["exp"] = self.owner.exp
        attr["coin"] = self.owner.coin
        attr["gold"] = self.owner.gold
        attr['combat'] = combat
        attr["skill_1"] = gamedataconfig.ALL_SKILL_INFO.get(skill_1)["skill_name"]
        attr["skill_2"] = gamedataconfig.ALL_SKILL_INFO.get(skill_2)["skill_name"]
        format_info = """【状态】\n等级:{level}\n经验:{exp}\n铜币:{coin}\n元宝:{gold}\n\n【{name}】\n战斗力:{combat}\n气血:{maxhp}\n普通攻击:{attack}\n法术攻击:{magic_attack}\n普通防御:{defend}\n法术防御:{magic_defend}\n命中:{hit}\n闪避:{dodge}\n暴击:{crit}\n韧性:{tenacity}\n致命:{deadly}\n速度:{speed}\n灵诀:{skill_1}\n神术:{skill_2}\n"""
        return format_info.format(**attr)

    def getFormationSerial(self):
        """获取伙伴阵法布置编号
        """
        try:
            return gamedataconfig.ALL_PARTNER_INFO[self.owner.template]["formation_serial"]
        except KeyError:
            return self.owner.template
    
    
    
    
    