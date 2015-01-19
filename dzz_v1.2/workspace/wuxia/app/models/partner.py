#coding:utf-8
'''
Created on 2014-8-14

Copyright 2014 www.9miao.com
'''
import mongoengine

class Partner(mongoengine.Document):
    """伙伴信息
    """
    partner_id = mongoengine.StringField(verbose_name="伙伴的唯一ID")
    roadnode = mongoengine.StringField(verbose_name="灵路当前节点")
    xiuwei = mongoengine.IntField(verbose_name="修为",default=0)
    explode = mongoengine.IntField(verbose_name="普通破防",default=0)
    magic_explode = mongoengine.IntField(verbose_name="法术破防",default=0)
    fatal = mongoengine.IntField(verbose_name="致命",default=0)
    speed = mongoengine.IntField(verbose_name="速度",default=0)
    prev_failed = mongoengine.BooleanField(verbose_name="是否突破失败",default=False)
    maxhp_comprehend = mongoengine.IntField(verbose_name="气血领悟等级",default=0)
    maxhp_break = mongoengine.IntField(verbose_name="气血突破等级",default=0)
    hit_comprehend = mongoengine.IntField(verbose_name="命中领悟等级",default=0)
    hit_break = mongoengine.IntField(verbose_name="命中突破等级",default=0)
    dodge_comprehend = mongoengine.IntField(verbose_name="闪躲领悟等级",default=0)
    dodge_break = mongoengine.IntField(verbose_name="闪躲突破等级",default=0)
    crit_comprehend = mongoengine.IntField(verbose_name="暴击领悟等级",default=0)
    crit_break = mongoengine.IntField(verbose_name="暴击突破等级",default=0)
    tenacity_comprehend = mongoengine.IntField(verbose_name="韧性领悟等级",default=0)
    tenacity_break = mongoengine.IntField(verbose_name="韧性突破等级",default=0)



    

    
