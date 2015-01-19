#coding:utf-8
'''
Created on 2014-7-23

Copyright 2014 www.9miao.com
'''
from gfirefly.dbentrust.util import ReadDataFromDB

#所有剧情信息
ALL_PLOT_INFO = {}
#所有NPC信息
ALL_NPC_INFO = {}
#所有的技能信息
ALL_SKILL_INFO = {}
#所有怪物信息
ALL_MONSTER_INFO = {}
#所有战斗配置信息
ALL_FIGHT_INFO = {}
#所有区域信息
ALL_AREA_INFO = {}
#所有场景信息
ALL_SCENE_INFO = {}
#所有的副本信息
ALL_FAM_INFO = {}
#所有的副本节点信息
ALL_FAMNODE_INFO = {}

#经验配置信息
EXPERIENCE_CONFIG = {}

#所有宠物的模板信息
ALL_PARTNER_INFO = {}
#主角的职业
LEAD_PROFESSION = 1
#最大上阵数
MAX_MEMBER=5

#所有的道具信息
ALL_TEMPLATE_INFO = {}
#所有的角色初始装备
ALL_APC_TEMPLATE = {}
#所有装备强化成长值
ALL_EQUIP_STREN_VALUE = {}
#所有装备品质属性加成
ALL_EQUIP_QUAL_ADDI_VALUE = {}
#所有装备强化基础值
ALL_EQUIP_STREN_INIT_COST = {}
#装备品质升级信息
ALL_EQUIP_QUAL_UPDATE = {}
#装备合成(进阶)信息
ALL_EQUIP_ADVANCE_INFO = {}

#所有灵路节点配置
ALL_ROAD_CONFIG = {}

#所有分享配置
ALL_SHARE_CONFIG = {}

#功法属性成长
ALL_GONGFA_GROW = {}
#功法突破
ALL_GONGFA_BREAK = {}

#竞技场机器人信息
ALL_AERNA_ROBOT = {}

def PlotInfoConfig():
    global ALL_PLOT_INFO
    resultlist = ReadDataFromDB('gamedata_plot')
    for _plot in resultlist:
        ALL_PLOT_INFO[_plot['plotid']]=_plot
        
def NPCInfoConfig():
    global ALL_NPC_INFO
    resultlist = ReadDataFromDB('gamedata_npcinfo')
    for _npc in resultlist:
        ALL_NPC_INFO[_npc['npc_id']]=_npc
        
def SkillInfoConfig():
    global ALL_SKILL_INFO
    resultlist = ReadDataFromDB('gamedata_skillinfo')
    for _skill in resultlist:
        ALL_SKILL_INFO[_skill['skill_id']]=_skill
        
def MonsterInfoConfig():
    global ALL_MONSTER_INFO
    resultlist = ReadDataFromDB('gamedata_monsterinfo')
    for _monster in resultlist:
#         _monster["skills"] = eval("[%s]"%_monster["skills"])
        ALL_MONSTER_INFO[_monster['monster_id']]=_monster
        
def FightInfoConfig():
    global ALL_FIGHT_INFO
    resultlist = ReadDataFromDB('gamedata_fightinfo')
    for _battle in resultlist:
        ALL_FIGHT_INFO[_battle['fight_id']]=_battle
        
def AreaInfoConfig():
    global ALL_AREA_INFO
    resultlist = ReadDataFromDB('gamedata_areainfo')
    for _area in resultlist:
        ALL_AREA_INFO[_area['area_id']]=_area
         
def SceneInfoConfig():
    global ALL_SCENE_INFO
    resultlist = ReadDataFromDB('gamedata_sceneinfo')
    for _scene in resultlist:
        ALL_SCENE_INFO[_scene['scene_id']]=_scene



def TemplateConfig():
    """获取所有道具配置信息
    """
    resultlist = ReadDataFromDB('gamedata_template')
    for _template in resultlist:
        ALL_TEMPLATE_INFO[_template['template_id']] = _template

def ApcConfig():
    """获取所有角色装备初始配置
    """
    resultlist = ReadDataFromDB('gamedata_equipmentconfig')
    for _apc in resultlist:
        ALL_APC_TEMPLATE[_apc['apc_id']] = _apc


def EquipQualAddiConfig():
    """获取装备品质属性加成
    """
    resultlist = ReadDataFromDB('gamedata_qualityaddition')
    for _quality in resultlist:
        quality, rank = _quality['quality'], _quality['rank']
        if quality not in ALL_EQUIP_QUAL_ADDI_VALUE:
            ALL_EQUIP_QUAL_ADDI_VALUE[quality] = {}
        ALL_EQUIP_QUAL_ADDI_VALUE[quality][rank] = _quality
    print ALL_EQUIP_QUAL_ADDI_VALUE

def EquipStrenGrowConfig():
    """获取装备强化成长值
    """
    resultlist = ReadDataFromDB('gamedata_strengthengrow')
    for _grow in resultlist:
        level, color = _grow['level'], _grow['color']
        if level not in ALL_EQUIP_STREN_VALUE:
            ALL_EQUIP_STREN_VALUE[level] = {}
        ALL_EQUIP_STREN_VALUE[level][color] = _grow
    
def EquipStrenInitCostConfig():
    """获取所有装备强化初始值
    """
    global ALL_EQUIP_STREN_INIT_COST
    resultlist = ReadDataFromDB('gamedata_strengtheninitconst')
    ALL_EQUIP_STREN_INIT_COST = resultlist[0] if resultlist else {}
    print ALL_EQUIP_STREN_INIT_COST

def EquipQualUpdate():
    """获取所有装备品质升级信息
    """
    resultlist = ReadDataFromDB('gamedata_equipqualityupdate')
    for _update in resultlist:
        quality, rank = _update['quality'], _update['rank']
        if quality not in ALL_EQUIP_QUAL_UPDATE:
            ALL_EQUIP_QUAL_UPDATE[quality] = {}
        ALL_EQUIP_QUAL_UPDATE[quality][rank] = _update


def EquipAdvanceConfig():
    """获取所有装备进阶信息
    """
    resultlist = ReadDataFromDB('gamedata_equipadvance')
    for _advance in resultlist:
        ALL_EQUIP_ADVANCE_INFO[_advance['source_equipid']] = _advance

    
def AllFamInfo():
    """获取所有的副本
    """
    global ALL_FAM_INFO
    resultlist = ReadDataFromDB('gamedata_fam')
    for _fam in resultlist:
        _fam['nodes'] = []
        ALL_FAM_INFO[_fam['fam_id']] = _fam
        
def AllFamNodeInfo():
    """获取所有的副本节点信息
    """
    global ALL_FAM_INFO,ALL_FAMNODE_INFO
    resultlist = ReadDataFromDB('gamedata_famnode')
    for _famnode in resultlist:
        ALL_FAMNODE_INFO[_famnode['node_id']]=_famnode
        ALL_FAM_INFO[_famnode['fam_id']]['nodes'].append(_famnode['node_id'])

def AllPartnersInfo():
    """获取所有宠物的模板信息
    """
    global ALL_PARTNER_INFO
    resultlist = ReadDataFromDB('gamedata_partners')
    for _p in resultlist:
        ALL_PARTNER_INFO[_p['partner_id']]=_p
        
        
def ALLExperienceConfig():
    """所有的经验配置信息
    """
    global EXPERIENCE_CONFIG
    resultlist = ReadDataFromDB('gamedata_experience')
    for _exp in resultlist:
        EXPERIENCE_CONFIG[_exp['level']]=_exp

def ALLRoadConfig():
    """所有灵路节点配置
    """
    resultlist = ReadDataFromDB('gamedata_road')
    for _r in resultlist:
        ALL_ROAD_CONFIG[_r['node_id']]= _r


def ALLShareConfig():
    """分享配置
    """
    resultlist = ReadDataFromDB('gamedata_share')
    for _s in resultlist:
        ALL_SHARE_CONFIG[_s['function']] = _s

def ALLGongfaGrowConfig():
    """功法属性成长
    """
    global ALL_GONGFA_GROW
    resultlist = ReadDataFromDB('gamedata_gongfa')
    ALL_GONGFA_GROW = resultlist[0] if resultlist else {}

def ALLGongfaBreakConfig():
    """功法突破
    """
    resultlist = ReadDataFromDB('gamedata_break')
    for _s in resultlist:
        ALL_GONGFA_BREAK[_s['level']] = _s
         
def ALLArenaRobotConfig():
    """功法突破
    """
    resultlist = ReadDataFromDB('gamedata_arenarobot')
    for _s in resultlist:
        ALL_AERNA_ROBOT[_s['robot_id']] = _s

    
    
    
    
