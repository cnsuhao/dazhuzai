#coding:utf-8
'''
Created on 2014-7-22
角色的剧情组件
Copyright 2014 www.9miao.com
'''
from app.core.component.Component import Component
from app.configdata import gamedataconfig


class CharacterPlotComponent(Component):
    
    def __init__(self,owner):
        """
        @param now_plot: 正在进行的剧情
        """
        Component.__init__(self, owner)
        self.now_plot = 0
        self.initData()
        
    def initData(self):
        """初始化数据
        """
        self.now_plot = self.owner.model.plot
        
    def openFunction(self):
        """开启功能
        """
        plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
        if not plot_info:
            return
        condition = plot_info.get("condition")
        if condition:
            self.owner.addRoleMessage([condition])
        
    def updatePlot(self,plot):
        """更新剧情
        """
        self.now_plot = plot
        self.owner.model.plot= plot

    def notice(self,action,**kw):
        """事件通知
        """
        #刚开始进入剧情
        if not self.now_plot:
            self.updatePlot("10001")
            #获取剧情的详细信息
            plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
            #获取剧情的开始描述
            plotstart = plot_info.get("plotstart").format(nickname=self.owner.model.nickname)
            #将描述条目划分开来
            plotstart_list = plotstart.split("||")
            self.owner.addRoleMessage(plotstart_list)
            self.openFunction()#通知新功能开启
            return
        #获取当前的剧情信息
        plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
        if plot_info is None:
            if action in ("proceed", "current"):
                return self.plotOver()
            return
        required = plot_info.get("required")
        required = required if required else "True"
        #如果满足剧情需求
        if eval(required):
            #获取剧情完成的对话
            plotend = plot_info.get("plotend").format(nickname=self.owner.model.nickname)
            plotend_list = plotend.split("||") if plotend else []
            #添加剧情完成的消息
            self.owner.addRoleMessage(plotend_list)
            #给予剧情完成的奖励
            reward = plot_info.get("reward")
            if reward:
                reward = eval(reward)
                self.owner.assets.getReward(reward)
#                 exec(reward)
            #自动进入下一个剧情
            next_plot = plot_info.get("next","")
            #更新当前剧情为下一个剧情
            if next_plot:
                self.updatePlot(next_plot)
            next_plot_info = gamedataconfig.ALL_PLOT_INFO.get(next_plot)
            if next_plot_info:
                next_plotstart = next_plot_info.get("plotstart").format(nickname=self.owner.model.nickname)
                #将描述条目划分开来
                next_plotstart_list = next_plotstart.split("||") if next_plotstart else []
                self.owner.addRoleMessage(next_plotstart_list)
            else:
                self.owner.addRoleMessage([self.plotOver()])
                return
                
            self.openFunction()#通知新功能开启
        else:
            if action in ("proceed", "current"):
                return self.getNowPlotDesc()
        return
        
    def getNowPlotDesc(self):
        """获取当前剧情介绍
        """
        plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
        if plot_info is None:
            return self.plotOver()
        plot_desc = plot_info.get("plotstart","")
        plotdesc_list = plot_desc.split("||")
        self.openFunction() #获取提示
        return "".join(plotdesc_list)
        
    def IsPlotFight(self):
        """是否可以进行剧情战斗
        """
        plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
        if not plot_info:
            return False
        if not plot_info.get("battleid"):
            return False
        return True
    
    def getPlotBattleId(self):
        """获取剧情战斗ID
        """
        plot_info = gamedataconfig.ALL_PLOT_INFO.get(self.now_plot)
        if plot_info:
            return plot_info.get("battleid")
        return ""

    def plotOver(self):
        """剧情结束
        """
        return "恭喜，剧情通关，后续精彩内容敬请期待！！！"

        
        
        
        
        
        
        
        