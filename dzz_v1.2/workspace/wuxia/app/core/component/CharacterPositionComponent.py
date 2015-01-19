#coding:utf-8
'''
Created on 2014-7-24
角色地理位置
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component
from app.configdata import gamedataconfig,msgconfig

class CharacterPositionComponent(Component):
    
    def __init__(self,owner):
        """初始化
        """
        Component.__init__(self, owner)
        self.scene = 0
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.scene = self.owner.model.scene
        if not self.scene:
            self.updateScene("10001")
        
    def updateScene(self,scene_id):
        """更新所在场景
        """
        self.scene=scene_id
        self.owner.model.scene=scene_id
        
    def getExportDesc(self):
        """获取出口描述
        """
        export_list = []
        scene_info = gamedataconfig.ALL_SCENE_INFO.get(self.scene)
        if scene_info.get("north"):
            north = gamedataconfig.ALL_SCENE_INFO.get(scene_info.get("north"))
            export_list.append("前方是%s\n"%(north.get("scene_name")))
        if scene_info.get("south"):
            south = gamedataconfig.ALL_SCENE_INFO.get(scene_info.get("south"))
            export_list.append("后方是%s\n"%(south.get("scene_name")))
        if scene_info.get("west"):
            west = gamedataconfig.ALL_SCENE_INFO.get(scene_info.get("west"))
            export_list.append("左边是%s\n"%(west.get("scene_name")))
        if scene_info.get("east"):
            east = gamedataconfig.ALL_SCENE_INFO.get(scene_info.get("east"))
            export_list.append("右边是%s\n"%(east.get("scene_name")))
        if export_list:
            return "".join(export_list)
        else:
            return "这里没有出口，得好好想想办法！"
        
    def getSceneDesc(self):
        """获取当前场景的描述
        """
        scene_info = gamedataconfig.ALL_SCENE_INFO.get(self.scene)
        if not scene_info:
            return msgconfig.getMsgFormat("not_scene_info")
        return scene_info.get("desc")
        
    def moveTo(self,direction):
        """场景内移动
        @param direction: 移动的方向
        """
#         start_scene = self.scene
#         scene_info = gamedataconfig.ALL_SCENE_INFO.get(self.scene)
#         print scene_info
#         next_scene = scene_info.get(direction)
#         if not next_scene:#如果没有出口
#             return msgconfig.getMsgFormat("not_scene_exit")
#         #更新到下一个场景
#         self.updateScene(next_scene)
#         #通知进行了移动的事件
        self.owner.plot.notice("moveTo",direction=direction)
        return #self.getSceneDesc()
            
        
        
        
        
    
    