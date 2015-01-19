#coding:utf8
'''
Created on 2014-6-18

Copyright 2014 www.9miao.com
'''
import xml.etree.ElementTree as ET
from mongoengine.queryset import DoesNotExist
from app.handler.service import wservice
from app.handler.api import *
from app.models.role import Role
from app.ability import pushmsg
from app.configdata import msgconfig

def toJson(xml_body):
    json_data = {}
    root = ET.fromstring(xml_body)
    for child in root:
        value = child.text
        json_data[child.tag] = value
    return json_data

def error_msg():
    from gfirefly.server.globalobject import GlobalObject
    debug = GlobalObject().webroot.config["DEBUG"]
    if debug:
        import traceback
        return {"result":False,"data":traceback.format_exc()}
    else:
        return {"result":False,"data":""}


class MessageAnalyzer:
    """消息分析器
    """
    
    def __init__(self,xmlmsg):
        """
        """
        self.request = toJson(xmlmsg)
        
    def getXmlArgs(self,argname):
        
        return self.request.get(argname)
    
    def actionGuess(self,openid,request_msg):
        """行为猜测
        """
        weiuser = Role.objects.get(openid=openid)
        next_command = weiuser.next_command
        if next_command:
            return next_command
        msg_args = request_msg.split(" ")
        msg = msg_args[0]
        if "百晓生" in msg or "help" in msg or "帮助" in msg:
            return "help"
        if "剧情" ==msg:
            return "nowplot"
        if "当前" == msg:
            return "current"
        if "地图" == msg:
            return "map"
        if "战斗" == msg:
            return "fight"
        if "npc" == msg.lower():
            return "npc"
        if "前"== msg:
            return "export_north"
        if "后"== msg:
            return "export_south"
        if "左"== msg:
            return "export_west"
        if "右"== msg:
            return "export_east"
        if "北"== msg:
            return "export_north"
        if "南"== msg:
            return "export_south"
        if "西"== msg:
            return "export_west"
        if "东"== msg:
            return "export_east"
        
        if "副本" == msg or "秘境"==msg:
            return "famlist"
        if "进入" in msg:
            return "enterfam"
        if "继续挑战"==msg or "继续探险"==msg:
            return "challenge"
        if "退出探险"==msg:
            return "exitfam"
        if "继续"==msg:
            return "proceed"
        if "查看"==msg:
            return "lookover"
        if "前往"==msg:
            return "go"

        if "布酒" == msg:
            return "formation_tavern"
        if "属技" == msg:
            return "property_skill"

        if "交谈" in msg:
            return "talkto"
        if "属性" == msg:
            return "property"
        if "阵型" == msg:
            return "formation_info"
        if "阵法" == msg:
            return "formation_info"
        if "更换阵法" in msg:
            return "change_formation"

        if "技能" == msg:
            return "skill"

        if "装备" == msg:
            return "equipchoice"

        if "酒馆" == msg or "返回酒馆" == msg:
            return "tavern"

        if "灵路" == msg:
            return "road"
        if "购买体力" == msg:
            return "buy_energy"

        if "签到" == msg:
            return "sign"
        if "兑换" == msg:
            return "exchange_info"
        if "打劫" == msg:
            return "rob_info"

        if "功法" == msg:
            return "gongfa"

        if "背包" == msg:
            return "package"

        if "充值" == msg:
            return "pay"

        if weiuser.prev_command == "formation_tavern":
            return "formation_tavern_choice"

        if weiuser.prev_command == "property_skill":
            return "property_skill_choice"

        if weiuser.prev_command == "famlist":
            return "enterfamid"

        if weiuser.prev_command == "enterarena":
            return "arenaname"


        if weiuser.prev_command == "skillchoice":
            return "skill"
        if weiuser.prev_command == "property":
            return "property"
            


        if weiuser.prev_command == "equipchoice":
            return "equipment"
        if weiuser.prev_command == "equipment":
            if "升品" in msg:
                return "update"
            if "自动强化" == msg:
                return "autostrengthen"
            if "强化" in msg:
                return "strengthen"
            if "进阶" in msg:
                return "advance"
            if msg.isdigit():
                return "equipment"

        if weiuser.prev_command == "tavern":
            return "partnerinfo"
        if weiuser.prev_command == "tavern_recruit":
            if "增加交情" == msg:
                return "friendshipmaterial"
        if weiuser.prev_command == "friendshipmaterial":
            return "addfriendship"
        if weiuser.prev_command == "addfriendship":
            if "继续增加" == msg:
                return "friendshipmaterial"

        if weiuser.prev_command == "road":
            return "road_explore"

        if weiuser.prev_command == "exchange_info":
            return "exchange"
        if weiuser.prev_command == "rob_info":
            return "rob"

        if weiuser.prev_command == "gongfa":
            return "gongfa_enter"
        if weiuser.prev_command == "gongfa_enter":
            return "gongfa_choice"
        if weiuser.prev_command == "gongfa_choice":
            return "gongfa_practice"

        return "internethelp"
        
    def analyze(self):
        """消息分析处理
        """
        print "#############start analyze##################"
        msgtype = self.getXmlArgs("MsgType")
        print "msgtype:%s"%msgtype
        ToUserName = self.getXmlArgs("ToUserName")
        FromUserName = self.getXmlArgs("FromUserName")
        
        #如果是事件消息
        if msgtype=="event":
            event = self.getXmlArgs("Event")
            #关注事件
            if event=="subscribe":
                response = wservice.call("subscribe",FromUserName,"")
                return pushmsg.produceResponsedMsg(FromUserName, ToUserName, response.get("data"))
            #取消关注事件
            elif event=="unsubscribe":
                response = wservice.call("unsubscribe",FromUserName,"")
                return pushmsg.produceResponsedMsg(FromUserName, ToUserName, response.get("data"))
            #菜单事件
            else:
                msg = self.getXmlArgs("EventKey")
        #如果是发送消息
        elif msgtype=="text":
            msg = self.getXmlArgs("Content")
        #如果是语音消息
        elif msgtype=="voice":
            msg = self.getXmlArgs("Recognition")
        
        try:#检测用户是否存在
            weiuser = Role.objects.get(openid=FromUserName)
        except DoesNotExist,e:#如果不存在,则关注
            response = wservice.call("subscribe",FromUserName,"")
            return pushmsg.produceResponsedMsg(FromUserName, ToUserName, response.get("data"))
        except Exception,e:
            response = error_msg()
            return pushmsg.produceResponsedMsg(FromUserName, ToUserName, response.get("data"))
        #用户操作行为分析
        action = self.actionGuess(FromUserName,msg)
        print "################actionGuess:[%s]#############:"%(action)
        ##########################
        try:
            response = wservice.call(action,FromUserName,msg)
        except Exception,e:#发送错误信息
            response = error_msg()
        ##########################
        return pushmsg.produceResponsedMsg(FromUserName, ToUserName, response.get("data"))
    
