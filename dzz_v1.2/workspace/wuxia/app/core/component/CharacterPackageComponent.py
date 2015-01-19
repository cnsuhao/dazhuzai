#coding:utf-8
'''
Created on 2014-9-23
角色的背包组件
Copyright 2014 www.9miao.com
'''
from mongoengine.queryset import DoesNotExist
from app.configdata import gamedataconfig
from app.models.role import Role
from app.core.component.Component import Component
from app.models.equipment import Material


class CharacterPackageComponent(Component):
    
    def __init__(self,owner):
        """初始化
        """
        Component.__init__(self, owner)
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.materials = self.owner.model.materials

    @property
    def package_map(self):
        """值为元祖，返回了list的位置，提供定位
        """
        return dict((m.materialid,(i,m.amount)) for i,m in enumerate(self.materials) if m.amount>0)

    def view(self):
        """查看
        """
        t = gamedataconfig.ALL_TEMPLATE_INFO
        m_dict = self.package_map
        m_list = sorted(m_dict.keys())
        info = ["%s.%s %s" %(i, t[k]["name"], m_dict[k][1]) for i,k in enumerate(m_list, start=1)]
        return "\n".join(info)

    def get_count(self, *mids):
        """返回mids包含的材料id数量
        """
        m_dict = self.package_map
        return [m_dict[mid][1] if mid in m_dict else 0 for mid in mids]

    def get_name(self, *mids):
        """返回材料名字
        """
        return [gamedataconfig.ALL_TEMPLATE_INFO[mid]["name"] for mid in mids]

    def update_count(self, materials):
        """更新数量{mid:count}
        """
        ms = set()
        for m in self.materials:
            if m.materialid in materials:
                m.amount += materials[m.materialid]
                ms.add(m.materialid)
        #没有的材料集合
        needs = set(materials.keys()) - ms
        for materialid in needs:
            self.materials.append(Material(materialid=materialid, amount=materials[materialid]))



   