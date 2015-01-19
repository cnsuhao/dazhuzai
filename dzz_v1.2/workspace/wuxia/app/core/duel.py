#coding:utf8
'''
Created on 2014-6-24
回合制战斗
Copyright 2014 www.9miao.com
'''
import random
from app.configdata import gamedataconfig

def produceFighterData(fighter):
    """
    """
#     info = {"name":fighter.getName(),
#             "hp":fighter.physique*10,
#             "level":fighter.getLevel(),
#             "force":fighter.force,
#             "physique":fighter.physique,
#             "iforce":fighter.iforce,
#             "dodge":fighter.dodge,
#             "skills":fighter.skills.all(),
#             "speed":(fighter.getLevel()*0.1+1)*fighter.dodge}
    return fighter.getBattleAttribut()


class Duel:
    
    def __init__(self,fighter1,fighter2):
        """
        """
        self.fighter1 = produceFighterData(fighter1)
        self.fighter2 = produceFighterData(fighter2)
        self.nowround = "第一回合"
        self.round_desc = []
        self.rounds = []
        self.result = 0
        
    def start(self):
        rounds = ["第一回合","第二回合","第三回合","第四回合","第五回合",
                 "第六回合","第七回合","第八回合","第九回合","第十回合"]
        for _round in rounds:
            #有任何一方重伤，结束战斗
            self.nowround = _round
            if self.fighter1["hp"]<=0 or self.fighter2["hp"]<=0:
                break
            self.round_desc.append("%s:\n"%self.nowround)
            self.doRound()
            self.rounds.append("".join(self.round_desc))
            self.round_desc=[]
        if self.fighter1["hp"]>self.fighter2["hp"]:
            self.result=1
            self.rounds.append("%s终于体力不支，重伤倒地！\n"%self.fighter2["name"])
        else:
            self.result=0
            self.rounds.append("%s终于体力不支，重伤倒地！\n"%self.fighter1["name"])
            
            
    def doRound(self):
        """
        """
        #比较速度
        if self.fighter1["speed"]>=self.fighter2["speed"]:
            self.settlement(self.fighter1, self.fighter2)
            self.settlement(self.fighter2, self.fighter1)
        else:
            self.settlement(self.fighter2, self.fighter1)
            self.settlement(self.fighter1, self.fighter2)
        
    def settlement(self,fighter1,fighter2):
        """战斗结算
        """
        if fighter1["hp"]<=0 or fighter2["hp"]<=0:
            return
        
        hp = fighter1["hp"]
        level = fighter1["level"]
        force = fighter1["force"]
        physique = fighter1["physique"]
        iforce = fighter1["iforce"]
        dodge = fighter1["dodge"]
        
        _hp = fighter2["hp"]
        _level = fighter2["level"]
        _force = fighter2["force"]
        _physique = fighter2["physique"]
        _iforce = fighter2["iforce"]
        _dodge = fighter2["dodge"]
        
        damage = 1
        if not fighter1["skills"]:
            skill = None
        else:
            skill = None
            skill_length = len(fighter1["skills"])
            skill_seq = range(skill_length)
            random.shuffle(skill_seq)
            for _sk_index in skill_seq:
                tmp_skill = fighter1["skills"][_sk_index]
                tmp_skill_info = gamedataconfig.ALL_SKILL_INFO.get(tmp_skill)
                print tmp_skill_info
                _skill_rate = random.randint(0,10000)
                if tmp_skill_info.get("rate")>=_skill_rate:
                    skill=tmp_skill
                    continue
        if skill:
            skill_info = gamedataconfig.ALL_SKILL_INFO.get(skill)
            skill_name=skill_info.get("skill_name")
            formula=skill_info.get("formula")
        else:
            skill_name="普通攻击"
            formula="damage=int(force*5-(_physique*1.0/force)*5);"
        exec(formula)
        fighter2["hp"]-=damage
        fighter_desc = "%s的[%s]对%s造成了%s点伤害\n"%(fighter1["name"],skill_name,fighter2["name"],damage)
        self.round_desc.append(fighter_desc)
        
        
def DoFight():
    pass
        
        
        
        
        
        