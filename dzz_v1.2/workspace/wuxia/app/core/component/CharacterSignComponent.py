#coding:utf-8
'''
Created on 2014-8-12
角色的竞技场组件
Copyright 2014 www.9miao.com
'''
import random
import datetime
import calendar
from collections import OrderedDict
from mongoengine.queryset import DoesNotExist
from app.configdata.globalconfig import DOMAIN, OAUTH2
from app.models.role import Sign
from app.models.arena import Arena
from app.core.component.Component import Component


EXCHANGE_LIST = OrderedDict({
        1: ("元宝",100)
    })
class CharacterSignComponent(Component):
    
    def __init__(self,owner):
        """初始化
        """
        Component.__init__(self, owner)
        self.now = datetime.datetime.now()
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.openid = self.owner.model.openid
        self.signModel = self.owner.model.sign
        if self.signModel is None:
            self.signModel = Sign(sign_time=datetime.datetime.fromtimestamp(0))
            self.owner.model.sign = self.signModel

        if (self.now.date() - self.signModel.sign_time.date()).days != 0:
            self.signModel.rob_time = 10
            self.signModel.robed_time = 0
            self.signModel.robed_lose = 0


    def __getattr__(self, name):
        return getattr(self.signModel, name)

    def already_sign_info(self):
        """已经签到信息
        """
        return "今天已签到，总积分%s。已连续签到%s天，本月累积签到%s天。\n提示：\n1.输入“打劫”可打劫其他玩家的积分\n2.输入“兑换”可用积分兑换重要物品" % (self.score, self.consecutive_day, self.accumulative_day)

    def sign_info(self, now):
        """签到信息
        """
        consecu_score = min(6,self.consecutive_day-1)*5
        accute = divmod(self.accumulative_day, 5)
        accute_score = self.accumulative_day if not accute[1] else 0
        last_day = now.day == calendar.mdays[now.month] #每月最后一天
        full_score = 200 if last_day and self.accumulative_day == now.day else 0

        score = 30+consecu_score+accute_score+full_score
        self.signModel.score += score
        info_tuple = (score, self.consecutive_day, consecu_score, self.accumulative_day, accute_score, full_score, self.score)
        info = "签到成功，获得%s积分，已连续签到%s天，连续签到奖励%s积分，本月累积签到%s天，累积签到积分奖励%s积分，本月全勤积分奖励%s积分，当前总积分%s。\n提示\n1.输入“打劫”可打劫其他玩家的积分\n2.输入“兑换”可用积分兑换重要物品" % info_tuple
        url = OAUTH2 % ('%s/share/%s/sign' %(DOMAIN, self.owner.model.openid))
        info += "\n<a href='%s'>签到分享有礼</a>" % url

        return info

    def sign(self):
        """签到
        """
        now = self.now
        if now.day == 1 or now.month - self.sign_time.month != 0 : #每月第一天，不同月，清空累计天数
            self.signModel.accumulative_day = 0

        delta = now.date() - self.sign_time.date()
        if delta.days == 0:
            return self.already_sign_info()
        elif delta.days == 1:
            self.signModel.accumulative_day += 1
            self.signModel.consecutive_day += 1
        else:
            self.signModel.accumulative_day += 1
            self.signModel.consecutive_day = 1
        self.signModel.sign_time = now
        return self.sign_info(now)


    def exchange_info(self):
        """积分兑换信息
        """
        info = ["目前拥有积分%s，可兑换物品如下：" % self.score]
        #暂时只有元宝
        for k, v in EXCHANGE_LIST.iteritems():
            info.append("%s.%s 兑换比例 %s:1" %(k, v[0],v[1]))
        info.append("输入物品序号+“@”+兑换数量即可兑换相应物品，例输入“1@2”可兑换2个元宝")
        return "\n".join(info)

    def exchange(self, seqno, num):
        """积分兑换
        """
        success = True
        cost, name = EXCHANGE_LIST[seqno][1] * num, EXCHANGE_LIST[seqno][0]
        if cost > self.score:
            success = False
            info = "您总共有%s积分，不够兑换哦，请重新输入，输入物品序号+“@”+兑换数量即可兑换相应物品，例输入“1@2”可兑换2个元宝" % self.score
        else:
            self.signModel.score -= cost
            info = "兑换%s个%s成功！剩余积分%s，继续兑换输入物品序号+“@”+兑换数量即可兑换相应物品，例输入“1@2”可兑换2个元宝" % (num, name, self.score)
            self.owner.model.gold += num
        return success, info

    def rob_info(self):
        """打劫信息
        """
        total = Arena.objects.count()
        try:
            rank = Arena.objects.get(openid=self.openid).rank
        except DoesNotExist:
            rank =  total+1
        left, right = max(1,rank-100), min(rank+100,total)
        ranges = range(left, right+1)
        ranges.remove(rank)
        ranks = random.sample(ranges, min(3,len(ranges)))
        #arenas = [Arena.objects.get(rank=r) for r in ranks]
        arenas = []
        for r in ranks:
            try:
                arenas.append(Arena.objects.get(rank=r))
            except:
                pass
        # arenas = []
        # gap = right - left + 1
        # for i in xrange(gap):
        #     r = random.randrange(left, right)
        #     if i == rank:
        #         break
        #     try:
        #         arena = Arena.objects.get(rank=r)
        #         arenas.append()
        #     except:
        #         pass

        info = []
        self.signModel.rob_user = []
        if arenas:
            info.append("您躲在了一棵树上，四下张望，发现了%s个看起来比较好欺负的人" % len(arenas))
            for i,arena in enumerate(arenas,1):
                info.append("%s.%s" %(i, arena.arenaname))
                self.signModel.rob_user.append(arena.openid)
        else:
            info.append("您躲在了一棵树上，四下张望，发现四处荒无人烟，无人可以打劫")
        info.append("今天剩余打劫次数%s次，今天您被人打劫了%s次，损失了%s积分\n提示：输入玩家序号可以打劫对应的人" %(self.rob_time, self.robed_time, self.robed_lose))
        return "\n".join(info)

    def calculate(self, robed_player, lscore, rscore):
        """打劫计算
        """
        ls = self.signModel.score + lscore
        self.signModel.score =  ls if ls > 0 else 0
        self.signModel.rob_time -= 1

        rs = robed_player.sign.signModel.score - rscore
        robed_player.sign.signModel.score = rs if rs>0 else 0
        robed_player.sign.signModel.robed_time += 1
        if rscore > 0:
            robed_player.sign.signModel.robed_lose += rscore

    def rob(self, robed_player):
        """打劫
        """
        if robed_player.sign.score <= 30:
            self.calculate(robed_player, 0, 0)
            return "对方实在是太可怜了，身无分文，你看他可怜，放他走了……"
        rc =self.owner.partners.getLeadCombat()
        rc2 = robed_player.partners.getLeadCombat()
        arenaname = robed_player.arena.arenaname
        success = random.random() < 1/(1+pow(10,float(rc2-rc)/(rc+rc2)*0.5))
        if success:
            score = min(random.randint(1, 2),robed_player.sign.signModel.score)
            if rc > rc2:
                info = "您从树上跳下，灵力爆射而出，仅仅用了一招就将“%s”打的口吐鲜血，高下立判，不费吹灰之力抢走了%s积分" % (arenaname,score)
            else:
                info = "您从树上跳下，出其不意，偷袭成功，将“%s”打晕，趁他没醒过来，抢走了%s积分" % (arenaname,score)
        else:
            # score = random.randint(0, 1)
            # if score == 1 and self.score:
            #     info = "您从树上跳下，却被“%s”的灵力深深的震撼的无法动弹，还没过招就已经输了，只好给他补偿%s积分，让他放过自己" % (arenaname,score)
            # else:
            #     info = "您从树上跳下，还没接近“%s”，就被他的气势所压倒，不敢出手，只能灰溜溜的跑掉" % arenaname
            # score = -score
            info = "您从树上跳下，却被“%s”的灵力深深的震撼的无法动弹，还没过招就已经输了，只好目送对方远去" % arenaname
            score = 0
        print 'rob',success,score
        self.calculate(robed_player, score, score)
        return info
                
















            



   






       
        
        
        
        
        
        
        
        
        
        
        