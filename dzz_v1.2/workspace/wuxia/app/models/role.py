#coding:utf-8
'''
Created on 2014-7-18
角色模型
Copyright 2014 www.9miao.com
'''
import mongoengine
from equipment import Material

class Formation(mongoengine.EmbeddedDocument):
    """队伍阵法
    """
    position_1 = mongoengine.IntField(verbose_name="位置1")
    position_2 = mongoengine.IntField(verbose_name="位置2")
    position_3 = mongoengine.IntField(verbose_name="位置3")
    position_4 = mongoengine.IntField(verbose_name="位置4")
    position_5 = mongoengine.IntField(verbose_name="位置5")
    position_6 = mongoengine.IntField(verbose_name="位置6")
    position_7 = mongoengine.IntField(verbose_name="位置7")
    position_8 = mongoengine.IntField(verbose_name="位置8")
    position_9 = mongoengine.IntField(verbose_name="位置9")

class Friendship(mongoengine.EmbeddedDocument):
    """招募交情
    """
    partner_id = mongoengine.IntField(verbose_name="伙伴的ID")
    friendship = mongoengine.IntField(verbose_name="交情")

class Sign(mongoengine.EmbeddedDocument):
    """签到
    """
    score = mongoengine.IntField(verbose_name="积分",default=0)
    consecutive_day = mongoengine.IntField(verbose_name="连续签到天数",default=0)
    accumulative_day = mongoengine.IntField(verbose_name="累计签到天数",default=0)
    sign_time = mongoengine.DateTimeField(verbose_name="签到时间")
    rob_time = mongoengine.IntField(verbose_name="打劫次数",default=10)
    robed_time = mongoengine.IntField(verbose_name="被打劫次数",default=0)
    robed_lose = mongoengine.IntField(verbose_name="打劫损失",default=0)
    rob_user = mongoengine.ListField(mongoengine.StringField(),verbose_name="打劫对方列表")

class Fam(mongoengine.EmbeddedDocument):
    """
    副本
    """
    fam_id = mongoengine.StringField(verbose_name="副本")
    surplustime = mongoengine.IntField(verbose_name="剩余次数",default=3)
    play_time = mongoengine.DateTimeField(verbose_name="时间")

class Role(mongoengine.Document):
    """角色的信息
    """
    openid = mongoengine.StringField(verbose_name="openID")
    nickname = mongoengine.StringField(verbose_name="用户昵称",default="")
    sex = mongoengine.IntField(verbose_name="性别,1m2f0u",default=1)
    profession = mongoengine.IntField(verbose_name="职业",default=0)
    level = mongoengine.IntField(verbose_name="等级",default=1)
    coin = mongoengine.IntField(verbose_name="铜钱",default=0)
    energy = mongoengine.IntField(verbose_name="体力",default=0)
    gold = mongoengine.IntField(verbose_name="元宝",default=0)
    exp = mongoengine.IntField(verbose_name="经验",default=0)
    energy_add_time = mongoengine.DateTimeField(verbose_name="上一次增加体力时间")
    energy_buytime = mongoengine.IntField(verbose_name="体力购买次数",default=1)
    plot = mongoengine.StringField(verbose_name="当前剧情",default="")
    scene = mongoengine.StringField(verbose_name="当前场景",default="")
    fam = mongoengine.StringField(verbose_name="当前副本",default="")
    famnode = mongoengine.StringField(verbose_name="当前节点",default="")
    clearance = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Fam),verbose_name="副本记录")
    message = mongoengine.ListField(mongoengine.StringField(),verbose_name="消息记录")
    partners = mongoengine.ListField(mongoengine.IntField(),verbose_name="角色伙伴")
    formation = mongoengine.EmbeddedDocumentField(Formation,verbose_name="角色阵法")
    sign = mongoengine.EmbeddedDocumentField(Sign,verbose_name="签到")
    friendships = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Friendship),verbose_name="伙伴友情")
    materials = mongoengine.ListField(mongoengine.EmbeddedDocumentField(Material),verbose_name="材料")
    subscribe_time = mongoengine.DateTimeField(verbose_name="入世时间")
    next_command = mongoengine.StringField(verbose_name="必要请求")
    prev_command = mongoengine.StringField(verbose_name="前一个状态")
    prev_objectid = mongoengine.IntField(verbose_name="操作对象的序号")
    prev_objectid2 = mongoengine.IntField(verbose_name="操作对象的序号")
    

class Share(mongoengine.Document):
    """记录分享信息
    """
    openid = mongoengine.StringField(verbose_name="openID")
    sign = mongoengine.DateTimeField(verbose_name="签到分享时间")
    fam = mongoengine.DateTimeField(verbose_name="秘境通关分享时间")
    

    
    