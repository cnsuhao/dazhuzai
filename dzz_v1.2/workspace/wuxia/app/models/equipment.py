#coding:utf-8
'''
Created on 2014-7-18

Copyright 2014 www.9miao.com
'''
import mongoengine

class EquipAttr(mongoengine.EmbeddedDocument):
    """装备属性
    """
    equipid = mongoengine.StringField(verbose_name="装备ID")
    strengthen_level = mongoengine.IntField(verbose_name="强化等级",default=1)
    advance_level = mongoengine.IntField(verbose_name="进阶等级",default=0)
    quality = mongoengine.IntField(verbose_name="物品品质",default=1)
    rank = mongoengine.IntField(verbose_name="物品品级",default=1)
    value1 = mongoengine.IntField(verbose_name="装备对应属性值1",default=0)
    value2 = mongoengine.IntField(verbose_name="装备对应属性值2",default=0)
    

class Material(mongoengine.EmbeddedDocument):
    """材料属性
    """
    materialid = mongoengine.StringField(verbose_name="材料ID")
    amount = mongoengine.IntField(verbose_name="数量",default=0)


class Equipment(mongoengine.Document):
    """装备信息
    """
    openid = mongoengine.StringField(verbose_name="openID")
    weapon = mongoengine.EmbeddedDocumentField(EquipAttr,verbose_name="武器")
    jacket = mongoengine.EmbeddedDocumentField(EquipAttr,verbose_name="上衣")
    belt = mongoengine.EmbeddedDocumentField(EquipAttr,verbose_name="腰带")



    
    
    