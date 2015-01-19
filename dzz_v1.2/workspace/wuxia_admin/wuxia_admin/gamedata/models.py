#coding:utf-8
"""
Copyright 2014 www.9miao.com
"""
from django.db import models
from django.contrib import admin
# Create your models here.

class Messages(models.Model):
    """消息格式
    """
    
    msgid = models.CharField(max_length=255,verbose_name="MSG ID",unique=True)
    message = models.TextField(max_length=1024,verbose_name="消息内容",null=True,blank=True)
    desc = models.TextField(max_length=1024,verbose_name="消息说明",null=True,blank=True)
    
    class Meta:
        verbose_name = "消息定制"
        verbose_name_plural = "消息定制"
        ordering = ('id','msgid')
        
    def __unicode__(self):
        return self.msgid
    
class MessageAdmin(admin.ModelAdmin):
    
    list_display = ('msgid','message')
    search_fields = ['msgid','message']
    
admin.site.register(Messages, MessageAdmin)

class Plot(models.Model):
    """剧情内容
    """
    plotid = models.CharField(max_length=255,verbose_name="剧情ID",unique=True)
    plotname = models.CharField(max_length=255,verbose_name="剧情名称",null=True,blank=True)
    plotdesc = models.CharField(max_length=1024,verbose_name="剧情简介",null=True,blank=True)
    plotstart = models.CharField(max_length=1024,verbose_name="剧情开始",null=True,blank=True)
    plotend = models.CharField(max_length=1024,verbose_name="剧情结束",null=True,blank=True)
    condition = models.CharField(max_length=1024,verbose_name="触发条件",null=True,blank=True)
    battleid = models.CharField(max_length=255,verbose_name="战斗ID",null=True,blank=True)
    required = models.CharField(max_length=1024,verbose_name="剧情需求",null=True,blank=True)
    reward = models.CharField(max_length=1024,verbose_name="剧情奖励",null=True,blank=True)
    next = models.CharField(max_length=255,verbose_name="下个剧情",null=True,blank=True)
    
    class Meta:
        verbose_name = "剧情内容"
        verbose_name_plural = "剧情内容"
        ordering = ('plotid','plotdesc')
        
    def __unicode__(self):
        return self.plotname
    
    
class PlotAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('plotid','plotname')
    search_fields = ['plotname','plotdesc']
    
admin.site.register(Plot, PlotAdmin)

###############################################
#NPC
###############################################

class NpcInfo(models.Model):
    """NPC信息
    """
    npc_id = models.CharField(max_length=50,verbose_name="NPC名称",unique=True)
    npc_name = models.CharField(max_length=50,verbose_name="NPC名称",null=True,blank=True)
    npc_desc1 = models.CharField(max_length=255,verbose_name="NPC对话1",null=True,blank=True)
    npc_desc2 = models.CharField(max_length=255,verbose_name="NPC对话2",null=True,blank=True)
    npc_desc3 = models.CharField(max_length=255,verbose_name="NPC对话3",null=True,blank=True)
    
    class Meta:
        verbose_name = "NPC信息"
        verbose_name_plural = "NPC信息"
        ordering = ('id','npc_name')
        
    def __unicode__(self):
        return self.npc_name
    
class NpcInfoAdmin(admin.ModelAdmin):
    
    list_display = ('id','npc_name')
    search_fields = ['npc_name']
    
admin.site.register(NpcInfo, NpcInfoAdmin)

###############################################
#技能
###############################################
class SkillInfo(models.Model):
    """技能信息
    """
    QUALITY = ((1,"基础"),
               (2,"入门"),
               (3,"精品"),
               (4,"绝世"),
               (5,"传说"))
    DAMAGE_TYPE = ((1,"物理伤害"),
               (2,"魔法伤害"))
    RULE = ((1,"敌方单体"),
               (2,"敌方全体"))
    skill_id = models.CharField(max_length=50,verbose_name="技能ID",unique=True)
    skill_name = models.CharField(max_length=50,verbose_name="技能名称",null=True,blank=True)
    skill_desc = models.CharField(max_length=255,verbose_name="技能描述",null=True,blank=True)
    quality = models.IntegerField(max_length=11,verbose_name="战斗类型",default=1,choices=QUALITY)
    rate = models.IntegerField(max_length=11,verbose_name="技能概率(10000)",default=5000,null=True,blank=True)
    cd = models.IntegerField(max_length=11,verbose_name="技能CD(10000)",default=0)
    damage_type = models.IntegerField(max_length=11,verbose_name="伤害类型",default=1,choices=DAMAGE_TYPE)
    rule = models.IntegerField(max_length=11,verbose_name="伤害规则",default=1,choices=RULE)
    formula = models.CharField(max_length=255,verbose_name="技能公式",null=True,blank=True)
    
    class Meta:
        verbose_name = "技能信息"
        verbose_name_plural = "技能信息"
        ordering = ('id','skill_name')
        
    def __unicode__(self):
        return self.skill_name
    
class SkillInfoAdmin(admin.ModelAdmin):
    
    list_display = ('skill_id','skill_name')
    search_fields = ['skill_name']
    list_filter = ('quality',)
    
admin.site.register(SkillInfo, SkillInfoAdmin)

###############################################
#怪物
###############################################

# class MonsterInfo(models.Model):
#     """怪物信息
#     """
#     QUALITY = ((1,"普通"),
#                (2,"强壮"),
#                (3,"精英"),
#                (4,"绝世"),
#                (5,"传说"))
#     monster_id = models.CharField(max_length=50,verbose_name="怪物ID",null=True,blank=True)
#     monster_name = models.CharField(max_length=50,verbose_name="怪物名称",null=True,blank=True)
#     monster_desc1 = models.CharField(max_length=255,verbose_name="怪物对话1",null=True,blank=True)
#     monster_desc2 = models.CharField(max_length=255,verbose_name="怪物对话2",null=True,blank=True)
#     monster_desc3 = models.CharField(max_length=255,verbose_name="怪物对话3",null=True,blank=True)
#     force = models.IntegerField(max_length=11,verbose_name="怪物力量",default=10,null=True,blank=True)
#     physique = models.IntegerField(max_length=11,verbose_name="怪物体质",default=10,null=True,blank=True)
#     iforce = models.IntegerField(max_length=11,verbose_name="怪物内力",default=10,null=True,blank=True)
#     dodge = models.IntegerField(max_length=11,verbose_name="侠客轻功",default=10,null=True,blank=True)
#     level = models.IntegerField(max_length=11,verbose_name="怪物等级",default=1,null=True,blank=True)
#     quality = models.IntegerField(max_length=11,verbose_name="怪物品质",default=1,choices=QUALITY)
#     skills = models.CharField(max_length=255,verbose_name="怪物技能",default="",blank=True,null=True)
#     
#     class Meta:
#         verbose_name = "怪物信息"
#         verbose_name_plural = "怪物信息"
#         ordering = ('id','monster_name')
#         
#     def __unicode__(self):
#         return self.monster_name

class MonsterInfo(models.Model):
    """怪物信息
    """
    monster_id = models.CharField(max_length=50,verbose_name="怪物ID",null=True,blank=True)
    monster_name = models.CharField(max_length=50,verbose_name="怪物名称",null=True,blank=True)
    monster_desc = models.CharField(max_length=255,verbose_name="怪物描述",null=True,blank=True)
    dander = models.IntegerField(max_length=11,verbose_name="初始能量",default=10,null=True,blank=True)
    hp = models.IntegerField(max_length=11,verbose_name="怪物血量",default=10,null=True,blank=True)
    level = models.IntegerField(max_length=11,verbose_name="怪物等级",default=10,null=True,blank=True)
    attack = models.IntegerField(max_length=11,verbose_name="怪物物攻",default=10,null=True,blank=True)
    magic_attack = models.IntegerField(max_length=11,verbose_name="怪物魔攻",default=10,null=True,blank=True)
    defend = models.IntegerField(max_length=11,verbose_name="怪物物防",default=10,null=True,blank=True)
    magic_defend = models.IntegerField(max_length=11,verbose_name="怪物魔防",default=10,null=True,blank=True)
    explode = models.IntegerField(max_length=11,verbose_name="物理破防",default=10,null=True,blank=True)
    magic_explode = models.IntegerField(max_length=11,verbose_name="魔法破防",default=10,null=True,blank=True)
    hit = models.IntegerField(max_length=11,verbose_name="怪物命中",default=10,null=True,blank=True)
    dodge = models.IntegerField(max_length=11,verbose_name="怪物闪避",default=10,null=True,blank=True)
    crit = models.IntegerField(max_length=11,verbose_name="怪物暴击",default=10,null=True,blank=True)
    tenacity = models.IntegerField(max_length=11,verbose_name="怪物韧性",default=10,null=True,blank=True)
    deadly = models.IntegerField(max_length=11,verbose_name="怪物致命",default=10,null=True,blank=True)
    speed = models.IntegerField(max_length=11,verbose_name="怪物速度",default=10,null=True,blank=True)
    ord_skill = models.CharField(max_length=11,verbose_name="普攻技能",default=10,null=True,blank=True)
    skill_1 = models.CharField(max_length=11,verbose_name="第一技能",default=10,null=True,blank=True)
    skill_2 = models.CharField(max_length=11,verbose_name="第二技能",default=10,null=True,blank=True)
    
     
    class Meta:
        verbose_name = "怪物信息"
        verbose_name_plural = "怪物信息"
        ordering = ('id','monster_name')
         
    def __unicode__(self):
        return self.monster_name
    
class MonsterInfoAdmin(admin.ModelAdmin):
    
    list_display = ('monster_id','monster_name')
    search_fields = ['monster_name']
    
admin.site.register(MonsterInfo, MonsterInfoAdmin)

###############################################
#战斗配置
###############################################
class FightInfo(models.Model):
    """战斗配置
    """
    fight_id = models.CharField(max_length=50,verbose_name="战斗的ID")
    desc = models.TextField(max_length=1024,verbose_name="战斗描述",null=True,blank=True)
    monster = models.CharField(max_length=1024,verbose_name="对手配置")
    reward = models.TextField(max_length=1024,verbose_name="奖励信息",null=True,blank=True)
    desc = models.CharField(max_length=1024,verbose_name="描述",null=True,blank=True)
    
    class Meta:
        verbose_name = "战斗配置"
        verbose_name_plural = "战斗配置"
        ordering = ('fight_id',)
    
class FightInfoAdmin(admin.ModelAdmin):
    
    list_display = ('fight_id','desc')
    
admin.site.register(FightInfo, FightInfoAdmin)


###############################################
#区域
###############################################

class AreaInfo(models.Model):
    """区域信息
    """
    area_id = models.CharField(max_length=50,verbose_name="区域ID")
    area_name = models.CharField(max_length=50,verbose_name="区域名称",null=True,blank=True)
    desc  = models.TextField(max_length=255,verbose_name="区域描述",null=True,blank=True)
    north = models.CharField(max_length=11,verbose_name="北方交界",default="",null=True,blank=True)
    south = models.CharField(max_length=11,verbose_name="南方交界",default="",null=True,blank=True)
    west = models.CharField(max_length=11,verbose_name="西方交界",default="",null=True,blank=True)
    east = models.CharField(max_length=11,verbose_name="东方交界",default="",null=True,blank=True)
    
    class Meta:
        verbose_name = "区域信息"
        verbose_name_plural = "区域信息"
        ordering = ('id','area_name')
        
    def __unicode__(self):
        return self.area_name
    
class AreaInfoAdmin(admin.ModelAdmin):
    
    list_display = ('id','area_name')
    search_fields = ['area_name',]
    
admin.site.register(AreaInfo, AreaInfoAdmin)


###############################################
#场景
###############################################

    
class SceneInfo(models.Model):
    """场景信息
    """
    AUTO_FIGHT_TYPE = ((0,"安全区域"),
             (1,"打怪区"),
             (2,"自由PK区"),
             (3,"阵营战斗区"))
    scene_id = models.CharField(max_length=50,verbose_name="场景ID",unique=True)
    scene_name = models.CharField(max_length=50,verbose_name="场景名称")
    desc  = models.TextField(max_length=255,verbose_name="场景描述")
    area = models.CharField(max_length=50,verbose_name="所属区域",default="",null=True,blank=True)
    north = models.CharField(max_length=11,verbose_name="北方出口",default="",null=True,blank=True)
    south = models.CharField(max_length=11,verbose_name="南方出口",default="",null=True,blank=True)
    west = models.CharField(max_length=11,verbose_name="西方出口",default="",null=True,blank=True)
    east = models.CharField(max_length=11,verbose_name="东方出口",default="",null=True,blank=True)
    npcs = models.CharField(max_length=255,verbose_name="场景NPC",default="",null=True,blank=True)
    battle = models.CharField(max_length=11,verbose_name="场景战斗",default="",null=True,blank=True)
    fight_type = models.IntegerField(max_length=11,verbose_name="战斗类型",default=0,choices=AUTO_FIGHT_TYPE,null=True,blank=True)
    
    class Meta:
        verbose_name = "场景信息"
        verbose_name_plural = "场景信息"
        ordering = ('id','scene_name')
    
class SceneInfoAdmin(admin.ModelAdmin):
    
    list_display = ('id','scene_name')
    search_fields = ['scene_name']
    list_filter = ('area',)
    
admin.site.register(SceneInfo, SceneInfoAdmin)

############################

class Template(models.Model):
    """道具总表
    """
    template_id = models.CharField(max_length=11,verbose_name="物品ID",unique=True)
    name = models.CharField(max_length=11,verbose_name="物品名称")
    level = models.IntegerField(verbose_name="使用等级",default=1)
    color = models.IntegerField(verbose_name="物品品质",default=1)
    attack = models.IntegerField(verbose_name="普通攻击",default=0,null=True,blank=True)
    magic_attack = models.IntegerField(verbose_name="法术攻击",default=0,null=True,blank=True)
    explode = models.IntegerField(verbose_name="普通破防",default=0,null=True,blank=True)
    magic_explode = models.IntegerField(verbose_name="法术破防",default=0,null=True,blank=True)
    defend = models.IntegerField(verbose_name="普通防御",default=0,null=True,blank=True)
    magic_defend = models.IntegerField(verbose_name="法术防御",default=0,null=True,blank=True)
    attack_speed = models.IntegerField(verbose_name="速度",default=0,null=True,blank=True)
    hp = models.IntegerField(verbose_name="气血",default=0,null=True,blank=True)
    friendship = models.IntegerField(verbose_name="交情",default=0,null=True,blank=True)

    class Meta:
        verbose_name = "道具总表"
        verbose_name_plural = "道具总表"
        ordering = ('template_id','name')

class TemplateAdmin(admin.ModelAdmin):
    search_fields = list_display = ('template_id', 'name', 'level', 'color')

admin.site.register(Template, TemplateAdmin)


class EquipmentConfig(models.Model):
    """角色装备配置
    """
    apc_id = models.IntegerField(verbose_name="职业ID")
    apc_name = models.CharField(max_length=11,verbose_name="职业名称")
    weapon = models.CharField(max_length=11,verbose_name="武器ID")
    jacket = models.CharField(max_length=11,verbose_name="上衣ID")
    belt = models.CharField(max_length=11,verbose_name="腰带ID")

    class Meta:
        verbose_name = "角色装备配置"
        verbose_name_plural = "角色装备配置"
        ordering = ('apc_id', 'apc_name')


class EquipmentConfigAdmin(admin.ModelAdmin):
    search_fields = list_display = ('apc_id', 'apc_name')

admin.site.register(EquipmentConfig, EquipmentConfigAdmin)


class StrengthenGrow(models.Model):
    """强化成长值
    """
    level = models.IntegerField(verbose_name="装备等级")
    color = models.IntegerField(verbose_name="品质")
    attack = models.FloatField(verbose_name="武器(普攻)")
    magic_attack = models.FloatField(verbose_name="武器(法攻)")
    defend = models.FloatField(verbose_name="上衣(普防)")
    magic_defend = models.FloatField(verbose_name="上衣(法防)")
    hp = models.FloatField(verbose_name="腰带(气血)")
    
    class Meta:
        verbose_name = "强化成长值"
        verbose_name_plural = "强化成长值"
        ordering = ('level', 'color')

class StrengthenGrowAdmin(admin.ModelAdmin):
    search_fields = list_display = ('level', 'color')

admin.site.register(StrengthenGrow, StrengthenGrowAdmin)

class StrengthenInitConst(models.Model):
    """装备强化费用基础值
    """
    weapon = models.IntegerField(verbose_name="武器")
    jacket = models.IntegerField(verbose_name="上衣")
    belt = models.IntegerField(verbose_name="腰带")

    class Meta:
        verbose_name = "装备强化基础值"
        verbose_name_plural = "装备强化基础值"

class StrengthenInitCostAdmin(admin.ModelAdmin):
    search_fields = list_display = ('weapon', 'jacket', 'belt')

admin.site.register(StrengthenInitConst, StrengthenInitCostAdmin)


class QualityAddition(models.Model):
    """品质属性加成
    """
    quality =models.IntegerField(verbose_name="装备品质(颜色)")
    rank = models.IntegerField(verbose_name="品级")
    attack = models.FloatField(verbose_name="武器(普攻)")
    magic_attack = models.FloatField(verbose_name="武器(法攻)")
    defend = models.FloatField(verbose_name="上衣(普防)")
    magic_defend = models.FloatField(verbose_name="上衣(法防)")
    hp = models.FloatField(verbose_name="腰带(气血)")
   
    class Meta:
        verbose_name = "品质属性加成"
        verbose_name_plural = "品质属性加成"
        ordering = ('quality', 'rank')

class QualityAdditionAdmin(admin.ModelAdmin):
    search_fields = list_display = ('quality', 'rank')

admin.site.register(QualityAddition, QualityAdditionAdmin)


class EquipQualityUpdate(models.Model):
    """装备品质升级
    """
    quality = models.IntegerField(verbose_name="装备品质(颜色)")
    rank = models.IntegerField(verbose_name="品级")
    material_id = models.CharField(max_length=11,verbose_name="所需材料ID")
    material_count = models.IntegerField(max_length=4,verbose_name="所需材料数量")
    update_cost = models.IntegerField(verbose_name="升品所需铜钱")
    update_quality = models.IntegerField(verbose_name="升品后装备品质(颜色)")
    update_rank = models.IntegerField(verbose_name="升品后装备品级")

    class Meta:
        verbose_name = "装备品质升级"
        verbose_name_plural = "装备品质升级"
        ordering = ('quality', 'rank')

class EquipQualityUpdateAdmin(admin.ModelAdmin):
    search_fields = ('quality', 'rank')
    list_display = ('quality', 'rank', 'material_id', 'material_count', 'update_cost')

admin.site.register(EquipQualityUpdate, EquipQualityUpdateAdmin)


class EquipAdvance(models.Model):
    """装备进阶(合成)
    """
    source_equipid = models.CharField(max_length=11,verbose_name="所需装备ID")
    source_equipid_name = models.CharField(max_length=64,verbose_name="所需装备名",default="")
    dest_equipid = models.CharField(max_length=11,verbose_name="目标装备ID")
    dest_equipid_name = models.CharField(max_length=64,verbose_name="目标装备名",default="")
    material1_id = models.CharField(max_length=11,verbose_name="材料1ID")
    material1_name = models.CharField(max_length=64,verbose_name="材料1名",default="")
    material1_count = models.IntegerField(max_length=4,verbose_name="所需材料1数量")
    material2_id = models.CharField(max_length=11,verbose_name="材料2ID")
    material2_name = models.CharField(max_length=64,verbose_name="材料2名",default="")
    material2_count = models.IntegerField(max_length=4,verbose_name="所需材料2数量")

    class Meta:
        verbose_name = "装备进阶"
        verbose_name_plural = "装备进阶"
        ordering = ('source_equipid', 'dest_equipid')

class EquipAdvanceAdmin(admin.ModelAdmin):
    search_fields = ('source_equipid', 'dest_equipid')
    list_display =  ('source_equipid', 'source_equipid_name','dest_equipid', 'dest_equipid_name',
                        'material1_id', 'material1_count', 'material2_id', 'material2_count')

admin.site.register(EquipAdvance, EquipAdvanceAdmin)

###############################################
#副本
###############################################
class Fam(models.Model):
    """副本
    """
    fam_id = models.CharField(max_length=11,verbose_name="副本的ID")
    fam_name = models.CharField(max_length=50,verbose_name="副本名称")
    desc  = models.TextField(max_length=255,verbose_name="副本描述",default="",null=True,blank=True)
    next_fam = models.CharField(max_length=11,verbose_name="下个副本",default="",null=True,blank=True)
     
    class Meta:
        verbose_name = "副本信息"
        verbose_name_plural = "副本信息"
        ordering = ('fam_id',)
         
         
class FamAdmin(admin.ModelAdmin):
     
    list_display = ('fam_id','fam_name')
    search_fields = ['fam_name','desc']
    
admin.site.register(Fam, FamAdmin)
 
class FamNode(models.Model):
    """副本节点
    """
    node_id = models.CharField(max_length=11,verbose_name="节点ID")
    fam_id = models.CharField(max_length=11,verbose_name="副本ID")
    node_name = models.CharField(max_length=50,verbose_name="节点名称")
    desc  = models.TextField(max_length=255,verbose_name="节点描述",null=True,blank=True)
    battleid = models.CharField(max_length=255,verbose_name="战斗ID")
    next_node = models.CharField(max_length=11,verbose_name="下个节点",default="",null=True,blank=True)
     
    class Meta:
        verbose_name = "副本节点"
        verbose_name_plural = "副本节点"
        ordering = ('node_id',)
    
class FamNodeAdmin(admin.ModelAdmin):
    
    list_display = ('node_id','node_name')
    search_fields = ['node_name','desc']
    
admin.site.register(FamNode, FamNodeAdmin)


###############################################
#职业
###############################################

class Partners(models.Model):
    """伙伴
    """
    partner_id = models.IntegerField(max_length=11,verbose_name="伙伴的ID")
    partner_name = models.CharField(max_length=11,verbose_name="伙伴名称")
    partner_desc = models.CharField(max_length=11,verbose_name="伙伴描述")
    ordinary_skill = models.CharField(max_length=11,verbose_name="普通攻击",default="",null=True,blank=True)
    skill_1 = models.CharField(max_length=11,verbose_name="第一技能",default="",null=True,blank=True)
    skill_2 = models.CharField(max_length=11,verbose_name="第二技能",default="",null=True,blank=True)
    passsive_skill = models.CharField(max_length=11,verbose_name="被动技能",default="",null=True,blank=True)
    maxhp = models.IntegerField(max_length=11,verbose_name="初始血量")
    attack = models.IntegerField(max_length=11,verbose_name="初始攻击")
    defend = models.IntegerField(max_length=11,verbose_name="初始防御")
    magic_attack = models.IntegerField(max_length=11,verbose_name="初始法攻")
    magic_defend = models.IntegerField(max_length=11,verbose_name="初始法防")
    hit = models.IntegerField(max_length=11,verbose_name="初始命中")
    dodge = models.IntegerField(max_length=11,verbose_name="初始闪避")
    crit = models.IntegerField(max_length=11,verbose_name="初始暴击")
    explode = models.IntegerField(max_length=11,verbose_name="外功破防")
    magic_explode = models.IntegerField(max_length=11,verbose_name="内功破防")
    fatal = models.IntegerField(max_length=11,verbose_name="致命")
    tenacity = models.IntegerField(max_length=11,verbose_name="坚韧")
    speed = models.IntegerField(max_length=11,verbose_name="速度",default=10,null=True,blank=True)
    
    hp_grow = models.FloatField(max_length=11,verbose_name="血量成长")
    attack_grow = models.FloatField(max_length=11,verbose_name="外功成长")
    defend_grow = models.FloatField(max_length=11,verbose_name="外防成长")
    magic_attack_grow = models.FloatField(max_length=11,verbose_name="内功成长")
    magic_defend_grow = models.FloatField(max_length=11,verbose_name="内防成长")
    
    hit_grow = models.FloatField(max_length=11,verbose_name="命中成长")
    dodge_grow = models.FloatField(max_length=11,verbose_name="闪避成长")
    crit_grow = models.FloatField(max_length=11,verbose_name="暴击成长")
    explode_grow = models.FloatField(max_length=11,verbose_name="外破成长")
    magic_explode_grow = models.FloatField(max_length=11,verbose_name="内破成长")
    fatal_grow = models.FloatField(max_length=11,verbose_name="致命成长")
    tenacity_grow = models.FloatField(max_length=11,verbose_name="坚韧成长")
    speed_grow = models.FloatField(max_length=11,verbose_name="速度成长")

    friendship = models.IntegerField(max_length=11,verbose_name="招募交情",default=0,null=True,blank=True)
    
    class Meta:
        verbose_name = "伙伴信息"
        verbose_name_plural = "伙伴信息"
        ordering = ('partner_id',)
        
        
class PartnersAdmin(admin.ModelAdmin):
    
    list_display = ('partner_id','partner_name')
    search_fields = ['partner_name','partner_desc']
    
admin.site.register(Partners, PartnersAdmin)


class Experience(models.Model):
    """经验配置表
    """
    level = models.IntegerField(max_length=11,verbose_name="当前等级")
    maxexp = models.IntegerField(max_length=11,verbose_name="最大经验")
    
    class Meta:
        verbose_name = "经验配置"
        verbose_name_plural = "经验配置"
        ordering = ('id',)
    
class ExperienceAdmin(admin.ModelAdmin):
    
    list_display = ('level','maxexp')
    
admin.site.register(Experience, ExperienceAdmin)

# class Friendship(models.Model):
#     """物品增加交情
#     """
#     template_id = models.CharField(max_length=11,verbose_name="物品ID",unique=True)
#     friendship = models.IntegerField(max_length=11,verbose_name="交情数")
#     class Meta:
#         verbose_name = "交情配置"
#         verbose_name_plural = "交情配置"
#         ordering = ('template_id',)

# class FriendshipAdmin(admin.ModelAdmin):
    
#     list_display = ('template_id','friendship')
    
# admin.site.register(Friendship, FriendshipAdmin)


class Road(models.Model):
    """灵路之旅配置
    """
    node_id = models.CharField(max_length=11,verbose_name="节点ID")
    node_name = models.CharField(max_length=50,verbose_name="节点名称")
    desc  = models.TextField(max_length=255,verbose_name="节点描述",null=True,blank=True)
    xiuwei = models.IntegerField(max_length=11,verbose_name="修为")
    battleid = models.CharField(max_length=255,verbose_name="战斗ID")
    node_reward = models.CharField(max_length=1024,verbose_name="节点奖励",null=True,blank=True)
    common_reward = models.IntegerField(max_length=11,verbose_name="普通奖励(经验值)",null=True,blank=True)
    next_node = models.CharField(max_length=11,verbose_name="下个节点",null=True,blank=True)
    class Meta:
        verbose_name = "灵路之旅配置"
        verbose_name_plural = "灵路之旅配置"
        ordering = ('node_id',)

class RoadAdmin(admin.ModelAdmin):
    list_display = ('node_id','node_name','node_reward')

admin.site.register(Road, RoadAdmin)

class Share(models.Model):
    """分享朋友圈
    """
    FUNCTIONS = (
                    (1, "签到"),
                    (2, "竞技场"),
                    (3, "祭拜财神"),
                    (4, "通关秘境")
                )
    function = models.IntegerField(max_length=11,verbose_name="功能",choices=FUNCTIONS)
    condition = models.CharField(max_length=11,verbose_name="分享条件")
    title = models.CharField(max_length=11,verbose_name="标题")
    hint = models.CharField(max_length=1024,verbose_name="分享提示语句")
    message = models.CharField(max_length=1024,verbose_name="对方看到")
    reward = models.IntegerField(verbose_name="额外奖励(单位:元宝)")

    class Meta:
        verbose_name_plural = verbose_name = "分享有礼"
        ordering = ('function',)

class ShareAdmin(admin.ModelAdmin):
    list_display = ('function','condition','reward')

admin.site.register(Share, ShareAdmin)

class Gongfa(models.Model):
    """功法属性成长
    """
    maxhp = models.IntegerField(verbose_name="气血")
    hit = models.IntegerField(verbose_name="命中")
    dodge = models.IntegerField(verbose_name="闪躲")
    crit = models.IntegerField(verbose_name="暴击")
    tenacity = models.IntegerField(verbose_name="韧性")
    comprehend_mid = models.CharField(max_length=11,verbose_name="领悟消耗物品id")
    break_mid = models.CharField(max_length=11,verbose_name="突破消耗物品id")

    class Meta:
        verbose_name_plural = verbose_name = "功法属性成长"

class GongfaAdmin(admin.ModelAdmin):
    list_display = ('maxhp','hit','dodge','crit','tenacity')

admin.site.register(Gongfa, GongfaAdmin)

class Break(models.Model):
    """功法突破
    """
    level = models.IntegerField(verbose_name="突破等级")
    ratio = models.FloatField(verbose_name="系数")
    need = models.IntegerField(verbose_name="突破所需")

    class Meta:
        verbose_name_plural = verbose_name = "功法突破"

class BreakAdmin(admin.ModelAdmin):
    list_display = ('level','ratio','need')

admin.site.register(Break, BreakAdmin)


class ArenaRobot(models.Model):
    """竞技场机器人信息
    """
    robot_id = models.CharField(max_length=50,verbose_name="怪物ID",null=True,blank=True)
    robot_name = models.CharField(max_length=50,verbose_name="怪物名称",null=True,blank=True)
    dander = models.IntegerField(max_length=11,verbose_name="初始能量",default=10,null=True,blank=True)
    hp = models.IntegerField(max_length=11,verbose_name="怪物血量",default=10,null=True,blank=True)
    level = models.IntegerField(max_length=11,verbose_name="怪物等级",default=10,null=True,blank=True)
    attack = models.IntegerField(max_length=11,verbose_name="怪物物攻",default=10,null=True,blank=True)
    magic_attack = models.IntegerField(max_length=11,verbose_name="怪物魔攻",default=10,null=True,blank=True)
    defend = models.IntegerField(max_length=11,verbose_name="怪物物防",default=10,null=True,blank=True)
    magic_defend = models.IntegerField(max_length=11,verbose_name="怪物魔防",default=10,null=True,blank=True)
    explode = models.IntegerField(max_length=11,verbose_name="物理破防",default=10,null=True,blank=True)
    magic_explode = models.IntegerField(max_length=11,verbose_name="魔法破防",default=10,null=True,blank=True)
    hit = models.IntegerField(max_length=11,verbose_name="怪物命中",default=10,null=True,blank=True)
    dodge = models.IntegerField(max_length=11,verbose_name="怪物闪避",default=10,null=True,blank=True)
    crit = models.IntegerField(max_length=11,verbose_name="怪物暴击",default=10,null=True,blank=True)
    tenacity = models.IntegerField(max_length=11,verbose_name="怪物韧性",default=10,null=True,blank=True)
    deadly = models.IntegerField(max_length=11,verbose_name="怪物致命",default=10,null=True,blank=True)
    speed = models.IntegerField(max_length=11,verbose_name="怪物速度",default=10,null=True,blank=True)
    ord_skill = models.CharField(max_length=11,verbose_name="普攻技能",default=10,null=True,blank=True)
    skill_1 = models.CharField(max_length=11,verbose_name="第一技能",default=10,null=True,blank=True)
    skill_2 = models.CharField(max_length=11,verbose_name="第二技能",default=10,null=True,blank=True)
    
     
    class Meta:
        verbose_name = "竞技场机器人"
        verbose_name_plural = "竞技场机器人"
        ordering = ('robot_id','robot_name')
         
    def __unicode__(self):
        return self.robot_name
    
class ArenaRobotAdmin(admin.ModelAdmin):
    
    list_display = ('robot_id','robot_name')
    search_fields = ['robot_name']
    
admin.site.register(ArenaRobot, ArenaRobotAdmin)


    