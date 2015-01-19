#coding:utf-8
'''
Created on 2014-8-15
战斗类
Copyright 2014 www.9miao.com
'''
from app.configdata.gamedataconfig import MAX_MEMBER
from app.configdata import gamedataconfig
import random

class Battle:
    
    def __init__(self,invaders,defenders):
        """
        @param invaders: 进攻方
        @param defenders: 防守方
        """
        self.invaders = invaders
        self.defenders = defenders
        self.invaders_list = []
        self.defenders_list = []
        self.warriors = {}
        self.warriors_list = []
        self.order = []
        self.round_desc = []
        self.rounds = []
        self.result = 0
        self.initBattlefield()
    
    def initBattlefield(self):
        """初始化战场
        """
        for position in range(1,MAX_MEMBER+1):
            warrior = self.invaders.get(position)
            if warrior:
                warrior_id = 10+position
                self.invaders_list.append(warrior_id)
                self.warriors[warrior_id] = warrior.getBattleAttribut()
        for position in range(1,MAX_MEMBER+1):
            warrior = self.defenders.get(position)
            if warrior:
                warrior_id = 20+position
                self.defenders_list.append(warrior_id)
                self.warriors[warrior_id] = warrior.getBattleAttribut()
        self.warriors_list = self.warriors.keys()
        
    def producedOrder(self):
        """生成出手顺序表
        """
        self.order = sorted(self.warriors_list,reverse=True,key=lambda warrior_id:self.warriors[warrior_id]["speed"])
        
    def checkOver(self):
        """检测战斗是否结束
        """
        return not(self.invaders_list and self.defenders_list)
#         return not(set.intersection(set(self.defenders_list),set(self.warriors_list)) and \
#                    set.intersection(set(self.invaders_list),set(self.warriors_list)))
    
    def producedResult(self):
        """生成战斗结果
        """
        if self.defenders_list:
            self.result = 0
        else:
            self.result = 1
            
    def skillCDProcess(self):
        """技能CD处理
        """
        # for warrior_id in self.warriors.keys():
        #     warrior = self.warriors.get(warrior_id)
        for warrior in self.warriors.values():
            if warrior["skill_cd"]["skill_2"]>0:
                warrior["skill_cd"]["skill_2"] -=1
                
    def someoneDied(self,warrior_id):
        """死亡后的处理
        """
        self.warriors_list.remove(warrior_id)
        if warrior_id>20:
            self.defenders_list.remove(warrior_id)
        else:
            self.invaders_list.remove(warrior_id)
        
    def start(self):
        rounds = ["第一回合","第二回合","第三回合","第四回合","第五回合",
                 "第六回合","第七回合","第八回合","第九回合","第十回合"]
        for i, _round in enumerate(rounds):
            #有任何一方重伤，结束战斗
            if self.checkOver():
                break
            self.round_desc.append("%s:\n"%_round)
            self.doRound()
            self.skillCDProcess()#技能CD处理
            if i < 3: #微信对文本消息长度有限制
                self.rounds.append("".join(self.round_desc))
            self.round_desc=[]
        if i > 3:
            self.rounds.append("......\n")
        self.producedResult()
        if self.result:
            self.rounds.append("战斗胜利")
        else:
            self.rounds.append("战斗失败\n真遗憾，快去强化，升品装备提升战斗力吧")
            
        
    def doRound(self):
        """开始战斗回合
        """
        self.producedOrder()
        for actor_id in self.order:
            if self.checkOver():
                break
            actor = self.warriors.get(actor_id)
            #如果攻击方已经死亡,跳过
            if actor["hp"]<=0:
                continue
            #技能选择
            #是否能触发主动技能
            if actor["dander"] >= 4:
                skill = actor["skill_1"]
                #self.warriors[actor_id]['dander']=0
            else:
                if actor["skill_cd"]["skill_2"]<=0:
                    skill = actor["skill_2"]
                    skill2_info = gamedataconfig.ALL_SKILL_INFO.get(skill)
                    self.warriors[actor_id]["skill_cd"]["skill_2"]=skill2_info['cd']
                else:
                    skill = actor["ord_skill"]
            skill_info = gamedataconfig.ALL_SKILL_INFO.get(skill)
            #技能目标选择规则
            rule = skill_info['rule']
            if rule==1:#攻击对方最前面的武将
                if actor_id>20:
                    victim_list = [self.invaders_list[0]]
                else:
                    victim_list = [self.defenders_list[0]]
            elif rule==2:#攻击敌方全体
                if actor_id>20:
                    victim_list = self.invaders_list
                else:
                    victim_list = self.defenders_list
            if not victim_list:
                break
            for victim_id in victim_list:
                self.settlement(actor_id, victim_id, skill)
                
                
    def settlement(self,actor_id,victim_id,skill):
        """计算技能产生的结果
        """
        actor = self.warriors.get(actor_id)
        victim = self.warriors.get(victim_id)
        skill_info = gamedataconfig.ALL_SKILL_INFO.get(skill)
        actor_name = actor["name"]
        victim_name = victim["name"]
        skill_name = skill_info["skill_name"]
        physical_damage = skill_info.get("damage_type") == 1 #伤害类型 1物理 2 魔法
        
        hp = actor["hp"]
        dander = actor["dander"]
        maxhp = actor["maxhp"]
        attack =  actor["attack"]
        defend = actor["defend"]
        magic_attack = actor["magic_attack"]
        magic_defend = actor["magic_defend"]
        explode = actor["explode"]
        magic_explode = actor["magic_explode"]
        hit = actor["hit"]
        dodge = actor["dodge"]
        crit = actor["crit"]
        tenacity = actor["tenacity"]
        deadly = actor["deadly"]
        level = actor["level"]
        
        _hp = victim["hp"]
        _maxhp = victim["maxhp"]
        _attack =  victim["attack"]
        _defend = victim["defend"]
        _magic_attack = victim["magic_attack"]
        _magic_defend = victim["magic_defend"]
        _explode = victim["explode"]
        _magic_explode = victim["magic_explode"]
        _hit = victim["hit"]
        _dodge = victim["dodge"]
        _crit = victim["crit"]
        _tenacity = victim["tenacity"]
        _deadly = victim["deadly"]
        _level = victim["level"]
        
        #判断命中
        if physical_damage:
            hitrate = int(max((hit*5)*1.0/((hit*5)+_dodge), 0.3)*100)
        else:
            hitrate = 1*100 #后期有buff处理
        now_hit_rate = random.randint(1,100)
        print hitrate,now_hit_rate
        if now_hit_rate>=hitrate:#没有命中
            fighter_desc = "【{0}】的【{1}】被【{2}】闪避\n".format(actor_name,skill_name,victim_name)
            self.round_desc.append(fighter_desc)
            if not physical_damage:
                self.warriors[actor_id]["dander"] = 0 #法术攻击后清0
            return

        #暴击率
        hit_crit = int((float(crit)/(crit+_tenacity*5))*100)
        random_crit = random.randint(1, 100)
        is_crit = hit_crit > random_crit
        #暴击伤害率
        crit_damage_rate = (1+float(deadly)/1000) if is_crit else 1

        #伤害计算
        level_press = 1+0.02*min(max(_level - level,-10),10) #等级压制率
        # formula=skill_info.get("formula")
        # exec(formula)
        #damage=attack * (1-min(0,max(float(_defend)/(explode*2+_defend) * level_press,0.9)))
        #damage=(attack+magic_attack) * (1-min(0,max(float(_magic_defend)/(magic_explode*2+_magic_defend) * level_press,0.9)))

        if physical_damage: #普通伤害
            damage_resistance = min(float(_defend)/(explode*2+_defend) * level_press,0.9)
            damage = attack * (1-damage_resistance)
        else:
            damage_resistance = min(float(_magic_defend)/(magic_explode*2+_magic_defend) * level_press,0.9)
            damage = (attack+magic_attack) * (1-damage_resistance)*(1+(dander-4)*0.1)

        damage = int(damage*crit_damage_rate)
        
        self.warriors[victim_id]["hp"] -= damage
        if physical_damage: #普通攻击命中增加dander
            self.warriors[actor_id]["dander"] += 1
            self.warriors[victim_id]["dander"] += 1
        else:
            self.warriors[actor_id]["dander"] = 0

        #记录伤害情况
        if damage>=0:
            crit_info = "【暴击】" if is_crit else ""
            fighter_desc = "【{0}】的【{1}】对【{2}】造成了 {3} 点{4}伤害\n".format(actor_name,skill_name,victim_name,damage,crit_info)
        else:
            fighter_desc = "【{0}】的【{1}】为【{2}】恢复了 {3} 点气血\n".format(actor_name,skill_name,victim_name,-damage)
        self.round_desc.append(fighter_desc)
        #判断死亡
        if self.warriors[victim_id]["hp"]<=0:
            self.someoneDied(victim_id)
            fighter_desc = "【{0}】因体力不支重伤倒地\n".format(victim_name)
            self.round_desc.append(fighter_desc)
        #完成一次战斗计算

class ArenaBattle(Battle):
    """竞技场战斗
    """
    def __init__(self,invaders,defenders,invaderteam,defenderteam):
        self.invaderteam = invaderteam
        self.defenderteam = defenderteam
        Battle.__init__(self,invaders,defenders)

    def initBattlefield(self):
        """初始化战场
        """
        for position in range(1,MAX_MEMBER+1):
            warrior = self.invaders.get(position)
            if warrior:
                warrior_id = 10+position
                self.invaders_list.append(warrior_id)
                attr = warrior.getBattleAttribut()
                attr["name"] = "%s-%s" %(self.invaderteam, attr["name"])
                self.warriors[warrior_id] = attr
        for position in range(1,MAX_MEMBER+1):
            warrior = self.defenders.get(position)
            if warrior:
                warrior_id = 20+position
                self.defenders_list.append(warrior_id)
                attr = warrior.getBattleAttribut()
                attr["name"] = "%s-%s" %(self.defenderteam, attr["name"])
                self.warriors[warrior_id] = attr
        self.warriors_list = self.warriors.keys()
        
        
def DoFightWithMonster(player,m_config_str):
    """与怪物进行战斗
    @param player: Character实例
    @param m_config_str: 怪物的配置信息字符串类似与{位置:怪物ID}
    """
    from app.core.monster import Monster
    invaders = player.formation.getBattleFormation()
    m_config = eval(m_config_str)
    defenders = {}
    for position in m_config.keys():
        monster_id = m_config.get(position)
        if monster_id:
            monster = Monster(monster_id)
            defenders[position] = monster
    return Battle(invaders, defenders)
            

def DoFightWithRole(player1,player2,teamname1,teamname2):
    """玩家间的战斗
    @param player1: Character实例
    @param player2: Character实例
    """
    invaders = player1.formation.getBattleFormation()
    defenders = player2.formation.getBattleFormation()
    return ArenaBattle(invaders, defenders,teamname1,teamname2)

def DoFightWithRobot(player, robot_id, teamname1,teamname2):
    """玩家和竞技场机器人
    """
    from app.core.monster import Robot
    invaders = player.formation.getBattleFormation()
    defenders = {}
    defenders[1] = Robot(robot_id)
    return ArenaBattle(invaders, defenders, teamname1,teamname2)


def DoFightPartnerWithMonster(partner,m_config_str):
    """与怪物进行战斗
    @param partner: partner实例
    @param m_config_str: 怪物的配置信息字符串类似与{位置:怪物ID}
    """
    from app.core.monster import Monster
    invaders = {1: partner}
    m_config = eval(m_config_str)
    defenders = {}
    for position in m_config.keys():
        monster_id = m_config.get(position)
        if monster_id:
            monster = Monster(monster_id)
            defenders[position] = monster
    return Battle(invaders, defenders)

    

    
