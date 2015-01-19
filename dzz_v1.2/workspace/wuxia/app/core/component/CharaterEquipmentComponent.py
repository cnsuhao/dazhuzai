#coding:utf-8
'''
Created on 2014-7-29
角色的装备组件
Copyright 2014 www.9miao.com
'''
from itertools import izip
from mongoengine.queryset import DoesNotExist
from app.core.component.Component import Component
from app.configdata import gamedataconfig
from app.models.equipment import EquipAttr, Equipment, Material

EQUIPMENT_KEY = ("weapon", "jacket", "belt")
EQUIPMENT_VALUE = ("武器", "衣服","腰带")
EQUIPMENT_ATTR = (("普通攻击","法术攻击"), ("普通防御","法术防御"),("气血",))
EQUIPMENT_ATTR_FIELD = (("attack","magic_attack"), ("defend","magic_defend"), ("hp",))

LEVEL = ('凡品', '良品', '优品', '极品', '绝品')
STRENGTHEN_LEVEL = 10

EQUIPMENT_QUALITY = dict(izip(xrange(1,4),("蓝色","紫色","橙色")))
UPDATE_LEVEL = 5

EQUIPMENT_LEVEL = dict(izip(xrange(5),(1, 20, 40, 60, 80)))

EQUIPMENT = dict(izip(EQUIPMENT_KEY, EQUIPMENT_VALUE))
EQUIPMENT_ATTR_DIC = dict(izip(EQUIPMENT_KEY, EQUIPMENT_ATTR))
EQUIPMENT_ATTR_FIELD_DIC = dict(izip(EQUIPMENT_KEY, EQUIPMENT_ATTR_FIELD))

def equip_type(equip_name):
    """根据装备名返回装备类型
    """
    equipment_key = None
    for k,v in izip(EQUIPMENT_KEY, EQUIPMENT_VALUE):
        if v in equip_name:
            equipment_key = k
            break
    return equipment_key

def equip_view(equip_model):
    """装备查看
    @param equip_model: 装备model
    """
    info = []
    for key, value, attrs in izip(EQUIPMENT_KEY, EQUIPMENT_VALUE, EQUIPMENT_ATTR):
        _e = equip_model[key]
        name = gamedataconfig.ALL_TEMPLATE_INFO[_e.equipid]["name"] #物品名称
        quality = CharacterEquipmentComponent.qualityLevel(_e.quality, _e.rank)
        strengthenLeval = CharacterEquipmentComponent.strengthenLeval(_e.strengthen_level)
        attrvalues = []
        for i, attr in enumerate(attrs,1):
            filed = "value" + str(i)
            attrvalues.append("%s+%s" % (attr, _e[filed]))
        attrvalues = " ".join(attrvalues)

        v = "%s：%s\n强化：%s\n升品：%s\n属性：%s\n\r\n" % (value, name, strengthenLeval, quality, attrvalues)
        info.append(v)
    #info.append("\n")
    
    info.append("输入“强化”可以查看强化信息，输入“升品”可以查看升品信息，输入“进阶”可以查看进阶信息")
    return ''.join(info)

def equip_create(profession, openid):
    """根据职业创建对应装备,包括伙伴装备
    @param profession: role的数据模型
    @param openid: openid或partnerid
    """
    equip_model = Equipment()
    equip_model.openid = openid
    #创建装备
    equipment_ids = [gamedataconfig.ALL_APC_TEMPLATE[profession].get(k,0) for k in EQUIPMENT_KEY]
    all_equips = izip(equipment_ids, EQUIPMENT_KEY, EQUIPMENT_ATTR_FIELD)
    for equip_id, equip_type, fields in all_equips:
        equipment = gamedataconfig.ALL_TEMPLATE_INFO[equip_id]
        #获取装备属性值,装备可能有多个属性
        values = {}
        for i, field in enumerate(fields,1):
            #装备初始属性值，装备等级， 强化等级，装备的物品品质 ,物品品级
            init, level, strengthen_level, quality, rank = equipment[field], 1, 1, equipment["color"], 1
            value = equip_attr_value(init, level, strengthen_level, quality, rank, field)
            values["value"+str(i)] = value
        equip_model[equip_type] = EquipAttr(equipid=equip_id, strengthen_level=strengthen_level, advance_level=level, quality=quality, rank=rank, **values)
    return equip_model

def equip_attr_value(init, level, strengthen_level, quality, rank, field):
    """装备的属性值
    @param init: 装备初始属性值
    @param level: 装备等级
    @param strengthen_level: 装备强化等级
    @param quality: 物品品质
    @param rank: 物品品级
    @param field: 装备属性(attack,magic_attack,...)

    当前属性=初始属性 +（强化等级-1）*强化成长值 + 品质属性加成
    """
    #强化成长值
    str_grow_value = gamedataconfig.ALL_EQUIP_STREN_VALUE[level][quality].get(field,0)
    #品质属性加成
    try:
        quality_addition = gamedataconfig.ALL_EQUIP_QUAL_ADDI_VALUE[quality][rank].get(field,0)
    except KeyError:
        quality_addition = 0
    return int(init+(strengthen_level-1)*str_grow_value+quality_addition)

def equip_strength_cost(level, key):
    """装备强化费用
    @param level: 强化等级
    @param key: 装备种类(weapon, jacket, ...)

    设当前强化等级为N，对应强化费用为YN ，对应强化总费用为ZN 
    强化费用公式:
    Y1=基础值（不同的部位有不同的基础值）
    YN=Y1 * 1.2^(N-1)    （2≤N≤19）
    YN=Y1 * 27* 1.1^(N-19)   （20≤N≤69）
    YN=Y1 * 3125* 1.05^(N-69)    (70≤N≤99）
    YN=Y1 * 13507 * 1.01^(N-99)   （N≥100）
    """
    #基础值
    init = gamedataconfig.ALL_EQUIP_STREN_INIT_COST[key]
    if level <= 19:
        cost = pow(1.2, level-1)
    elif level <= 69:
        cost = 27*pow(1.1, level-19)
    elif level <= 99:
        cost = 3125*pow(1.05, level-69)
    else:
        cost = 13507*pow(1.01, level-99)
    return int(init*cost)

def equip_strength_view(equip_model):
    """装备强化查看
    @param equip_model: 装备model
    """
    info = []
    for key, value, attrs, fields in izip(EQUIPMENT_KEY, EQUIPMENT_VALUE, EQUIPMENT_ATTR, EQUIPMENT_ATTR_FIELD):
        _e = equip_model[key]
        #强化到下一级, +1
        next_strengthen_level = _e.strengthen_level+1
        #名称
        name = gamedataconfig.ALL_TEMPLATE_INFO[_e.equipid]["name"]
        #装备品质
        quality = CharacterEquipmentComponent.qualityLevel(_e.quality, _e.rank)
        #装备强化值
        strengthenLeval = CharacterEquipmentComponent.strengthenLeval(next_strengthen_level)
        #装备真实等级
        advance_real_level = CharacterEquipmentComponent.advanceRealLevel(_e.advance_level)
        #装备显示等级
        advance_level = CharacterEquipmentComponent.advanceLevel(_e.advance_level)

        attrvalues = []
        for attr, field in izip(attrs, fields):
            #装备属性初始值
            init = gamedataconfig.ALL_TEMPLATE_INFO[_e.equipid][field]
            #装备属性值
            attrvalue = equip_attr_value(init, advance_real_level, next_strengthen_level, _e.quality, _e.rank, field)
            attrvalues.append("%s+%s" % (attr, attrvalue))
        attrvalues = " ".join(attrvalues)
        
        #装备强化费用
        cost = equip_strength_cost(next_strengthen_level, key)
        v = "%s：%s\n强化消耗：%s铜钱\n强化结果：%s(%s)\n强化属性：%s\n\r\n" % (value, name, cost, name, strengthenLeval, attrvalues)
        info.append(v)
    #info.append("\n")
    info.append("操作提示：\n1.输入“强化”+“装备部位”可以强化该部位装备，如输入“强化武器”，将对武器进行强化\n2.输入“自动强化”可以自动将所有装备强化5次")
    return ''.join(info)

def equip_advance_view(equip_model):
    """装备进阶查看
    """
    info = []
    for key, value, attrs, fields in izip(EQUIPMENT_KEY, EQUIPMENT_VALUE, EQUIPMENT_ATTR, EQUIPMENT_ATTR_FIELD):
        _e = equip_model[key]
        #进阶装备信息
        advance_info = gamedataconfig.ALL_EQUIP_ADVANCE_INFO[_e.equipid]
        srcname = gamedataconfig.ALL_TEMPLATE_INFO[_e.equipid]["name"]
        #进阶后新装备ID
        new_equipid = advance_info["dest_equipid"]
        #进阶后新装备名称
        name = gamedataconfig.ALL_TEMPLATE_INFO[new_equipid]["name"]
        #进阶所需材料1名
        material1_name = gamedataconfig.ALL_TEMPLATE_INFO[advance_info["material1_id"]]["name"]
        #进阶所需材料1数量
        material1_count = advance_info["material1_count"]
        #进阶所需材料2名
        material2_name = gamedataconfig.ALL_TEMPLATE_INFO[advance_info["material2_id"]]["name"]
        #进阶所需材料2数量
        material2_count = advance_info["material2_count"]
        #进阶后装备品质
        advance_quality = gamedataconfig.ALL_TEMPLATE_INFO[new_equipid]["color"]

        #进阶后装备品质
        quality = CharacterEquipmentComponent.qualityLevel(advance_quality, _e["rank"])
        #进阶的装备等级
        advance_level = CharacterEquipmentComponent.advanceLevel(_e["advance_level"]+1)
        #装备实际等级
        advance_real_level = CharacterEquipmentComponent.advanceRealLevel(_e["advance_level"]+1)
        #装备强化值
        strengthenLeval = CharacterEquipmentComponent.strengthenLeval(_e["strengthen_level"])
        #新装备属性初始值
        attrvalues = []
        for attr, field in izip(attrs, fields):
            init = gamedataconfig.ALL_TEMPLATE_INFO[new_equipid][field]
            #装备属性值
            attrvalue = equip_attr_value(init, advance_real_level, _e["strengthen_level"], advance_quality, _e["rank"], field)
            attrvalues.append("%s+%s" % (attr, attrvalue))
        attrvalues = " ".join(attrvalues)
       
        v = "%s：%s\n进阶消耗：%s %s %s%s\n进阶结果：%s (条件:人物%s) (%s)(%s)\n进阶属性：%s\n\r\n" % (value, srcname, material1_name, material1_count, material2_name, material2_count, \
                        name,  advance_level, quality, strengthenLeval, attrvalues)
        info.append(v)

    #info.append("\n")
    info.append("操作提示：输入“进阶”+“装备部位”可以强化该部位装备，如输入“进阶武器”，将对武器进行进阶")
    return ''.join(info)

def equip_update_view(equip_model):
    """装备升品查看
    """
    info = []
    for key, value, attrs, fields in izip(EQUIPMENT_KEY, EQUIPMENT_VALUE, EQUIPMENT_ATTR, EQUIPMENT_ATTR_FIELD):
        _e = equip_model[key]
        #名称
        name = gamedataconfig.ALL_TEMPLATE_INFO[_e.equipid]["name"]
        #升品材料信息
        update_info = gamedataconfig.ALL_EQUIP_QUAL_UPDATE[_e["quality"]][_e["rank"]]
        #升品所需材料名
        material_name = gamedataconfig.ALL_TEMPLATE_INFO[update_info["material_id"]]["name"]
        #升品所需材料数量
        material_count = update_info["material_count"]
        #升品所需铜钱
        update_cost = update_info["update_cost"]
        #升品后装备品质
        update_quality = update_info["update_quality"]
        #升品后装备品级
        update_rank = update_info["update_rank"]

        #升品后装备品质
        quality = CharacterEquipmentComponent.qualityLevel(update_quality, update_rank)
        #升品后的装备等级
        advance_level = CharacterEquipmentComponent.advanceLevel(_e["advance_level"])
        #实际装备属性等级
        advance_real_level = CharacterEquipmentComponent.advanceRealLevel(_e["advance_level"])
        #装备强化值
        strengthenLeval = CharacterEquipmentComponent.strengthenLeval(_e["strengthen_level"])

        attrvalues = []
        for attr, field in izip(attrs, fields):
            #装备属性初始值
            init = gamedataconfig.ALL_TEMPLATE_INFO[_e["equipid"]][field]
            #装备属性值
            attrvalue = equip_attr_value(init, advance_real_level, _e["strengthen_level"], update_quality, update_rank, field)
            attrvalues.append("%s+%s" % (attr, attrvalue))
        attrvalues = " ".join(attrvalues)

        v = "%s：%s\n升品消耗：%s %s 铜钱 %s\n升品结果：%s(%s)\n升品属性：%s\n\r\n" % (value, name, material_name, material_count, update_cost, \
                                    name, quality, attrvalues)
        info.append(v)
    #info.append("\n")
    info.append("操作提示：输入“升品”+“装备部位”可以强化该部位装备，如输入“升品武器”，将对武器进行升品")
    return ''.join(info)


class CharacterEquipmentComponent(Component):
    
    def __init__(self,owner):
        """
        """
        Component.__init__(self, owner)
        self.powner = self.owner.owner
        self.equip_model = None
        self.equip_type = None
        self.initData()

    # def __getattr__(self, name):
    #     return getattr(self.equip_model[self.equip_type], name)
        
    def initData(self):
        """初始化数据
        """
        self.autoUpdateModel()

    def save(self):
        """装备保存,提供给外部奖励调用
        """
        if self.equip_model is not None:
            self.equip_model.save()

    def autoUpdateModel(self):
        """自动更新装备数据模型,装备类型
        """
        if self.equip_model is None:
            openid = self.owner.partner_id
            # openid = self.owner.model.openid
            try:
                equip_model = Equipment.objects.get(openid=openid)
            except DoesNotExist:
                print 'create equip_model'
                profession = self.owner.template
                equip_model = equip_create(profession, openid)
                equip_model.save()
            self.equip_model = equip_model

    def view(self):
        """查看装备
        """
        return equip_view(self.equip_model)

    def advanceView(self):
        """进阶查看
        """
        return equip_advance_view(self.equip_model)

    def updateView(self):
        """升品查看
        """
        return equip_update_view(self.equip_model)

    def strengthenView(self):
        """强化查看
        """
        return equip_strength_view(self.equip_model)

    @property
    def strengthenLevel(self):
        return self.equip_model[self.equip_type].strengthen_level

    def updateEquip(self, equip_model, equip_type=None):
        """更新装备数据模型,装备类型
        """
        self.equip_model = equip_model
        self.equip_type = equip_type

    def updateEquipType(self, equip_type):
        """更新装备类型
        """
        self.equip_type = equip_type

    def isTopAdvance(self):
        """是否进阶到最高级
        """
        level = self.equip_model[self.equip_type].advance_level
        return CharacterEquipmentComponent.isTopAdvanceLevel(level)

    @classmethod
    def isTopAdvanceLevel(cls, advance_level):
        """判断装备是否进阶到最高级
        """
        return advance_level == len(EQUIPMENT_LEVEL)

    @classmethod
    def advanceLevel(cls, advance_level):
        """返回装备等级
        """
        ADVANCE = ("新手装", "20级", "30级", "40级", "50级")
        if cls.isTopAdvanceLevel(advance_level):
            return "装备已进阶到最高级"
        return ADVANCE[advance_level-1]

    @classmethod
    def advanceRealLevel(cls, advance_level):
        """根据装备(1-5)返回实际装备等级
        """
        return EQUIPMENT_LEVEL[advance_level-1]

    def isTopUpdate(self):
        quality = self.equip_model[self.equip_type].quality
        rank = self.equip_model[self.equip_type].rank
        return CharacterEquipmentComponent.isTopUpdateLevel(quality, rank)


    @classmethod
    def isTopUpdateLevel(cls, quality, rank):
        """根据品质和品级判断是否是最高级
        """
        return quality == len(EQUIPMENT_QUALITY) and rank == UPDATE_LEVEL

    @classmethod
    def qualityLevel(cls, quality, rank):
        """根据品质和品级返回装备品质信息
        """
        if cls.isTopUpdateLevel(quality, rank):
            return "装备已升品到最高级"
        return "%s%s星" % (EQUIPMENT_QUALITY[quality], rank)

    @classmethod
    def strengthenLeval(cls, level):
        """根据level返回强化等级
        """
        if cls.isTopStrenLevel(level):
            return "装备已强化到最高级"
        else:
            big, lit = divmod(level, STRENGTHEN_LEVEL)
            if lit == 0:
                big -= 1
                lit = 10
        return "%s%s级" % (LEVEL[big], lit)

    @classmethod
    def isTopStrenLevel(cls, level):
        """是否已经是强化最高级
        """
        return level >= len(LEVEL)*STRENGTHEN_LEVEL

    def isTopStren(self):
        level = self.equip_model[self.equip_type].strengthen_level
        return CharacterEquipmentComponent.isTopStrenLevel(level)

    def strenRoleLevelEnough(self):
        """进阶判断任务等级是否足够(暂时伙伴使用主角的等级)
        """
        return self.powner.model.level >= self.equip_model[self.equip_type].strengthen_level+1

    def moneyEnough(self):
        """强化时判断金钱是否充足
        """
        level = self.equip_model[self.equip_type].strengthen_level+1
        return self.powner.model.coin >= equip_strength_cost(level, self.equip_type)

    def getEquipAttrValue(self):
        """根据装备model获取属性信息
        """
        equipment = self.equip_model[self.equip_type]
        equipid = equipment.equipid
        level = equipment.strengthen_level
        advance_real_level = self.advanceRealLevel(equipment.advance_level)
        quality = equipment.quality
        rank = equipment.rank
        #装备属性初始值
        fields = EQUIPMENT_ATTR_FIELD_DIC[self.equip_type]
        attrs = EQUIPMENT_ATTR_DIC[self.equip_type]
        attrvalues = []
        for i, _ in enumerate(izip(attrs, fields),1):
            attr, field = _
            init = gamedataconfig.ALL_TEMPLATE_INFO[equipid][field]
            attrvalue = equip_attr_value(init, advance_real_level, level, quality, rank, field)
            #更新属性值
            equipment["value"+str(i)] = attrvalue
            attrvalues.append("%s+%s" % (attr, attrvalue))
        attrvalues = " ".join(attrvalues)
        
        return {
            "name": gamedataconfig.ALL_TEMPLATE_INFO[equipid]["name"], #装备名称
            "value": attrvalues, #装备所有属性值
            "equip_type": EQUIPMENT[self.equip_type], #装备类型
            "strengthen_level": self.strengthenLeval(level), #装备强化等级
            "equip_attr": EQUIPMENT_ATTR_DIC[self.equip_type], #装备属性
            "quality_level": self.qualityLevel(quality, rank),  #品质属性
            "equip_level": self.advanceLevel(equipment.advance_level) #装备等级
        }
                   
        
    def strengthen(self):
        """装备强化
        """
        level = self.equip_model[self.equip_type].strengthen_level+1
        equipid = self.equip_model[self.equip_type].equipid
        #更新等级
        self.equip_model[self.equip_type].strengthen_level = level
        #扣除铜钱
        self.powner.model.coin -= equip_strength_cost(level, self.equip_type)
        print 'strengthen ok------------'
        attr = self.getEquipAttrValue()
        
        info = "强化成功\n%s：%s\n强化等级：%s\n强化属性：%s" % (attr["equip_type"], attr["name"], attr["strengthen_level"], attr["value"])
                                        
        return info

    def updateMoneyEnough(self, cost):
        """升品判断铜钱是否足够
        """
        return self.powner.model.coin >= cost

    def updateMaterialEnough(self, material_id, material_count):
        """升品时判断材料是否足够
        由于需要更新数量，所有放在最后判断
        """
        for m in self.powner.model.materials:
            if m.materialid ==  material_id and m.amount >= material_count:
                #更新数量
                m.amount -= material_count
                return True

    def update(self):
        """装备升品查看
        @ret flag{Boolean},info{str}
        """
        success = False
        equipid = self.equip_model[self.equip_type].equipid
        quality = self.equip_model[self.equip_type].quality
        rank = self.equip_model[self.equip_type].rank

        #升品材料信息
        update_info = gamedataconfig.ALL_EQUIP_QUAL_UPDATE[quality][rank]

        #升品所需铜钱
        update_cost = update_info["update_cost"]
        if not self.updateMoneyEnough(update_cost):
            return success, "升品失败 铜钱不足"

        #升品所需材料ID
        material_id = update_info["material_id"]
        #升品所需材料数量
        material_count = update_info["material_count"]
        if not self.updateMaterialEnough(material_id, material_count):
            return success, "升品失败 材料不足"

        success = True
        #扣除铜钱
        self.powner.model.coin -= update_cost
        #升品后装备品质
        self.equip_model[self.equip_type].quality = update_info["update_quality"]
        #升品后装备品级
        self.equip_model[self.equip_type].rank = update_info["update_rank"]
        #装备名称
        attr = self.getEquipAttrValue()
        info = "升品成功\n%s：%s升品等级：%s\n升品属性：%s" % (attr["equip_type"], attr["name"], attr["quality_level"], attr["value"])
                                        
        return success, info

    def advanceRoleLevelEnough(self, level):
        """进阶判断任务等级是否足够
        """
        return self.powner.model.level >= level

    def advanceMaterialEnough(self, materials):
        """进阶所需材料是否充足
        @param: materials{dict}
        """
        count = 0
        ms = []
        needs = len(materials)
        for m in self.powner.model.materials:
            if m.materialid in materials and m.amount >= materials[m.materialid]:
                count += 1
                ms.append((m, materials[m.materialid]))
            if len(ms) == needs:
                break

        if len(ms) != needs:
            return False
        else:
            #所有材料都满足，更新数量
            for model, count in ms:
                model.amount -= count
            return True

    def advance(self):
        """装备进阶
        """
        success = False
        equipid = self.equip_model[self.equip_type].equipid
        advance_info = gamedataconfig.ALL_EQUIP_ADVANCE_INFO[equipid]
        #新装备使用等级
        role_level = gamedataconfig.ALL_TEMPLATE_INFO[advance_info["dest_equipid"]]["level"]

        if not self.advanceRoleLevelEnough(role_level):
            return success, "进阶失败 人物等级不足"
        materials = {}
        #进阶所需材料ID, 进阶所需材料数量
        materials[advance_info["material1_id"]] = advance_info["material1_count"]
        materials[advance_info["material2_id"]] = advance_info["material2_count"]
        if not self.advanceMaterialEnough(materials):
            return success, "进阶失败 材料不足"
        success = True
        #更新新装备ID
        self.equip_model[self.equip_type].equipid = advance_info["dest_equipid"]
        #更新进阶等级
        self.equip_model[self.equip_type].advance_level += 1
        attr = self.getEquipAttrValue()
        #更新属性值
        info = "进阶成功\n%s：%s\n强化等级：%s\n升品等级：%s\n进阶属性：%s" % (attr["equip_type"], attr["name"], attr["strengthen_level"], attr["quality_level"], attr["value"])
                                    
        return success, info


    def getBattleAttribute(self):
        """获取战斗属性
        """
        attr = {}
        for equip_type, keys in izip(EQUIPMENT_KEY, EQUIPMENT_ATTR_FIELD):
            for i, key in enumerate(keys,1):
                if key == "hp":
                    key = "maxhp"
                field = "value" + str(i)
                attr[key] = self.equip_model[equip_type][field]
        print "getBattleAttribute",attr
        return attr


    def addMaterial(self, materials):
        """增加材料(物品)
        @param materials{dict}: {materialId{str}:count{int}}, {材料ID,材料数量}
        """
        ms = set()
        for m in self.powner.model.materials:
            if m.materialid in materials:
                m.amount += materials[m.materialid]
                ms.add(m.materialid)
        #没有的材料集合
        needs = set(materials.keys()) - ms
        for materialid in needs:
            self.powner.model.materials.append(Material(materialid=materialid, amount=materials[materialid]))

        msg_list = []
        for mid, mcount in materials.iteritems():
            info = "获得:%s 数量:%d" %(gamedataconfig.ALL_TEMPLATE_INFO[mid]["name"], mcount)
            msg_list.append(info)
        self.powner.addRoleMessage(msg_list)
        #减少外部奖励调用
        self.powner.model.save()

