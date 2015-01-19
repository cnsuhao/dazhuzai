#coding:utf-8
'''
Created on 2014-7-18

Copyright 2014 www.9miao.com
'''
import time
from datetime import datetime
from gfirefly.server.globalobject import webserviceHandle
from gfirefly.server.globalobject import GlobalObject
from flask import request, make_response
from flask import render_template
from flask import abort, redirect, url_for
from mongoengine.queryset import DoesNotExist
from app.models.role import Role, Share, Pay, Warn
from app.utils.hashtools import checkMD5, checkAppSignature
from app.handler.analyzer import MessageAnalyzer, toJson
from app.configdata import msgconfig,globalconfig,mongoconfig,gamedataconfig
from app.configdata.globalconfig import getOpenID, getUserInfo
from app.ability.pushmsg import pushWeixinMessage

from app.models.admin import init_admin

@webserviceHandle("/do", methods=['GET', 'POST'])
def do():
    """这里主要消息接口
    """
    signature = request.args.get("signature","")
    timestamp = request.args.get("timestamp","")
    nonce = request.args.get("nonce","")
    #这里做平台的接入，没有做安全检测
    if not checkMD5(signature,timestamp,nonce):
        return "check failed"
    if request.args.get("echostr"):
        return request.args.get("echostr")
    print request.form
    
    if not request.data and not request.form:
        return "failed"
    if request.data:
        xmldoc = request.data
    else:
        xmldoc = dict(request.form).keys()[0]
    print xmldoc
    ma = MessageAnalyzer(xmldoc)
    msg = ma.analyze()
    return msg


@webserviceHandle("/clear", methods=['GET', 'POST'])
def clear():
    """重新读取配置信息
    """
    Role.objects.all().delete()
    return "success"

@webserviceHandle("/reload", methods=['GET', 'POST'])
def load():
    """重新读取配置信息
    """
    configure()
    return "success"


def configure():
    """数据配置
    """
    #读入全局的配置信息
    globalconfig.init_global_config()
    #配置mongodb
    mongoconfig.init_Mongo_Conns()
    #读入消息格式配置
    msgconfig.MSGConfig()
    #读入剧情信息
    gamedataconfig.PlotInfoConfig()
    gamedataconfig.NPCInfoConfig()
    gamedataconfig.SkillInfoConfig()
    gamedataconfig.MonsterInfoConfig()
    gamedataconfig.FightInfoConfig()
    gamedataconfig.AreaInfoConfig()
    gamedataconfig.SceneInfoConfig()
    #读入副本信息
    gamedataconfig.AllFamInfo()
    gamedataconfig.AllFamNodeInfo()
    gamedataconfig.AllPartnersInfo()
    #经验配置信息
    gamedataconfig.ALLExperienceConfig()

    #读入装配配置信息
    gamedataconfig.TemplateConfig()
    gamedataconfig.ApcConfig()
    gamedataconfig.EquipQualAddiConfig()
    gamedataconfig.EquipStrenGrowConfig()
    gamedataconfig.EquipStrenInitCostConfig()
    gamedataconfig.EquipQualUpdate()
    gamedataconfig.EquipAdvanceConfig()
    
    #灵路配置信息
    gamedataconfig.ALLRoadConfig()
    #分享配置
    gamedataconfig.ALLShareConfig()
    #功法配置
    gamedataconfig.ALLGongfaGrowConfig()
    gamedataconfig.ALLGongfaBreakConfig()

    #竞技场机器人
    gamedataconfig.ALLArenaRobotConfig()

def init():
    app = GlobalObject().webroot
    init_admin(app)

#读入配置数据信息
configure()
init()


_REQTITLE = ('我也要签到', '我也要挑战', '我也要祭拜财神', '我也要通关秘境')
_HEADIMG = ('dazhuzai.jpg', 'male.png', 'female.png')
_CATEGORY = {'sign':1, 'arena':2, 'god':3, 'fam':4 }
@webserviceHandle("/share/<openid>/<category>", methods=['GET', 'POST'])
def share(openid, category):
    myopenid = request.cookies.get('myopenid')
    if myopenid is None:
        code = request.args.get('code','')
        info = getOpenID(code)
        print 'share openid info:',info
        myopenid = info.get("openid")

    myself = openid == myopenid
    role = Role.objects.get(openid=openid)
    if not role.nickname or not role.sex:
        user = getUserInfo(openid)
        role.nickname = user.get('nickname','')
        role.sex = user.get('sex', 0)
        role.save()

    if myself:
        vexist = 1
    else:
        try:
            Role.objects.get(openid=myopenid)
        except DoesNotExist:
            vexist = 0
        else:
            vexist = 1

    index = _CATEGORY[category.strip()]
    today = datetime.today()
    config = gamedataconfig.ALL_SHARE_CONFIG[index]
    share = {
        'nickname': role.nickname,
        'headimg': _HEADIMG[role.sex],
        'title': config['title'],
        'share': "分享一下" if myself else "打个酱油，分享一下",
        'hint': config['hint'] if myself else config['message'],
        'message': config['message'],
        'domain': globalconfig.DOMAIN,
        'today': "%s年%s月%s日" % (today.year, today.month, today.day),
        'reqtitle': _REQTITLE[index-1],
        'vexist': vexist,
        'myself': myself,
        'rewardUrl': "%s/reward/%s/%s" %(globalconfig.DOMAIN, category, openid)
    }
    response = make_response(render_template('share.html', share=share))
    if myopenid is not None:
        print 'share set cookie:',myopenid
        response.set_cookie('myopenid', myopenid, max_age=3600)
    return response


@webserviceHandle("/reward/<category>/<openid>")
def reward(category, openid):
    gold = gamedataconfig.ALL_SHARE_CONFIG[_CATEGORY[category]]["reward"]
    now = datetime.now()
    try:
        share = Share.objects.get(openid=openid)
    except DoesNotExist:
        share = Share(openid=openid)
        
    t = getattr(share, category)
    if t is None or (now - t).days !=0: #不是同一天
        Role.objects(openid=openid).update(inc__gold=gold)
    setattr(share, category, now)
    share.save()
    return "success"

@webserviceHandle("/config")
def config():
    print str(GlobalObject().webroot.config)
    return 'success'

@webserviceHandle("/debug")
def debug():
    if request.args.get('debug') == 'true':
        GlobalObject().webroot.config["DEBUG"] = True
    else:
        GlobalObject().webroot.config["DEBUG"] = False
    return 'DEBUG:'+str(GlobalObject().webroot.config["DEBUG"])


@webserviceHandle("/token")
def token():
    return globalconfig.get_Access_token()


@webserviceHandle("/")
def index():
    """首页"""
    #urls = [url_for("share",openid="oYs3pjiHCppgscIy-od-8moh8gOU",category=category) for category in _CATEGORY]
    return render_template('index.html')



@webserviceHandle("/push")
def push():
    openid = request.args.get("oid")
    content = request.args.get("c")
    if openid and content:
        try:
            pushWeixinMessage(openid, content)
            return "SUCCESS"
        except:
            import traceback
            return traceback.format_exc()
    else:
        return "args error"





    






