#coding:utf-8
'''
Created on 2014-7-25
怪物信息
Copyright 2014 www.9miao.com
'''
from app.configdata import gamedataconfig

class Monster:
    
    def __init__(self,monster_id):
        """怪物信息
        """
        self.monster_id = monster_id
        self.info = gamedataconfig.ALL_MONSTER_INFO
        self.name = "monster_name"
        
    def getBattleAttribut(self):
        """获取战斗属性
        """
        monster_info = dict(self.info.get(self.monster_id))
        monster_info['maxhp'] = monster_info["hp"]
        monster_info["name"] = monster_info[self.name]
        monster_info["died"] = 0
        #monster_info['dander'] = 0 #怒气
        skill_cd = gamedataconfig.ALL_SKILL_INFO[monster_info["skill_2"]]["cd"]
        monster_info["skill_cd"] = {"skill_2":skill_cd}
        return monster_info
    
    def getCombat(self, info=None):
        """获取战斗力
        """
        if info is None:
            info = self.info.get(self.monster_id)

        return int(((info["attack"]+float(info["magic_attack"])/3)*0.5+(info["explode"]+float(info["magic_explode"])/2)*1+ \
                    (info["magic_defend"]+float(info["defend"])/2)*0.4+info["hp"]*0.2+ \
                    (info['crit']+info['tenacity']+info['hit'])*2)*pow(1.01, info["level"]-1)
                )


class Robot(Monster):

    def __init__(self,monster_id):
        """机器人信息
        """
        self.monster_id = monster_id
        self.info = gamedataconfig.ALL_AERNA_ROBOT
        self.name = "robot_name"
    
    
    
        