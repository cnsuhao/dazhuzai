#coding:utf-8
'''
Created on 2014-8-4
角色的副本进度信息
Copyright 2014 www.9miao.com
'''
from datetime import datetime
from app.models.role import Fam
from app.configdata.globalconfig import DOMAIN, OAUTH2
from app.core.component.Component import Component
from app.configdata import gamedataconfig,msgconfig

FAM_DEFAULT_TIME = 3

class CharacterFamComponent(Component):
    """角色的副本进度信息
    """
    
    def __init__(self,owner):
        """
        """
        Component.__init__(self, owner)
        self.clearance = []
        self.fam = ""
        self.famnode = ""
        self.initData()
        
    def initData(self):
        """初始化角色信息
        """
        self.clearance = self.owner.model.clearance
        self.fam = self.owner.model.fam
        self.famnode = self.owner.model.famnode
        self.fam_dict = dict(((f.fam_id,i) for i, f in enumerate(self.clearance)))
        if not self.clearance:
            self.addClearance("80000")

    def updateFam(self,fam_id):
        """更新副本ＩＤ
        """
        self.fam=fam_id
        self.owner.model.fam = fam_id
        if not fam_id:
            return
        fam = self.clearance[self.fam_dict[fam_id]]
        
        now = datetime.now()
        if (now.date() - fam.play_time.date()).days != 0: #不是同一天
            fam.surplustime = FAM_DEFAULT_TIME -1
            fam.play_time = datetime.now()
        else:
            if fam.surplustime <= 0:
                return False
            fam.surplustime -= 1
        return True
        
    def updateFamNode(self,fam_node):
        """更新副本节点ＩＤ
        """
        self.famnode=fam_node
        self.owner.model.famnode = fam_node
        
    def addClearance(self,fam_id):
        """更新通关记录
        """
        if fam_id not in self.fam_dict:
            self.clearance.append(Fam(fam_id=fam_id,play_time=datetime.now()))
            self.fam_dict[fam_id] = len(self.clearance)-1
            self.owner.model.clearance = self.clearance
        
    def getFamList(self):
        """副本信息
        """
        if self.fam:
            return self.getFamInfo()
        fam_info_list = []
        #获取前面通关了的副本
        now = datetime.now()
        for _fam in self.clearance:
            fam_info = gamedataconfig.ALL_FAM_INFO.get(_fam.fam_id)
            if (now.date() - _fam.play_time.date()).days != 0:
                time = FAM_DEFAULT_TIME
            else:
                time = _fam.surplustime
            fam_desc = "【%s】(%s)已开启 今天剩余次数%s\n"%(fam_info['fam_name'], _fam.fam_id, time)
            fam_info_list.append(fam_desc)
        
        help_msg = "\n输入 秘境ID 如80000 进入80000秘境"
        fam_info_list.append(help_msg)
        return "".join(fam_info_list)
    
    def getFamInfo(self):
        """获取副本信息
        """
        fam_info = gamedataconfig.ALL_FAM_INFO.get(self.fam)
        fam_nodes = fam_info.get("nodes",[])
        node_info_list=[]
        for _node in fam_nodes:
            node_info = gamedataconfig.ALL_FAMNODE_INFO.get(_node)
            node_name = node_info.get("node_name","")
            if _node==self.famnode:
                node_info_list.append("【%s】当前\n"%(node_name))
            else:
                node_info_list.append("【%s】\n"%(node_name))
        help_msg = "\n输入　继续探险　或　退出探险"
        node_info_list.append(help_msg)
        return "".join(node_info_list) 
    
    def enterFam(self,fam_id):
        """进入副本
        """
        if fam_id not in self.fam_dict:
            return "该秘境还未开启，请重新选择"
        if not self.updateFam(fam_id):
            return "挑战次数已用完，明天再来吧[微笑]"
        fam_info = gamedataconfig.ALL_FAM_INFO.get(fam_id)
        fam_nodes = fam_info.get("nodes",[])
        self.updateFamNode(fam_nodes[0])
        return self.getFamInfo()
        
    
    def challenge(self):
        """继续探险,副本战斗
        """
        from app.core.monster import Monster
        from app.core.battle import DoFightWithMonster
        node_info = gamedataconfig.ALL_FAMNODE_INFO.get(self.famnode)
        battleid = node_info.get("battleid")
        
        battle_info = gamedataconfig.ALL_FIGHT_INFO.get(battleid)
        m_config_str = battle_info.get("monster")
        
        #战斗描述
        fight_desc = battle_info.get("desc")
        fight = DoFightWithMonster(self.owner, m_config_str)
        fight.start()
        info = fight_desc+"\n"+"\n".join(fight.rounds)
        
        #判断战斗结果
        #失败
        if not fight.result:
            self.owner.addRoleMessage([self.getFamInfo()])
        #战斗胜利
        else:
            next_node = node_info.get("next_node","")
            reward = battle_info.get("reward")
            #给予战斗奖励
            if reward:
                reward = eval(reward)
                self.owner.assets.getReward(reward)
            #判断是否通关
            #通关
            if not next_node:
                fam_info = gamedataconfig.ALL_FAM_INFO.get(self.fam)
                fam_name = fam_info.get("fam_name")
                next_fam = fam_info.get("next_fam")
                self.addClearance(next_fam)
                self.updateFam("")
                self.updateFamNode("")
                url = OAUTH2 % ('%s/share/%s/fam' %(DOMAIN, self.owner.model.openid))
                self.owner.addRoleMessage(["你太棒了，恭喜你，通关【%s】\n<a href='%s'>通关分享有礼</a>" %(fam_name,url)])
            else:
                self.updateFamNode(next_node)
                self.owner.addRoleMessage([self.getFamInfo()])
        return info
    
    def exitFam(self):
        """退出副本
        """
        self.updateFam("")
        self.updateFamNode("")
        return "你退出了秘境"
    
    
            
            
            


