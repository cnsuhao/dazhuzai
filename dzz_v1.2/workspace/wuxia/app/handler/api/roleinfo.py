#coding:utf8
'''
Created on 2014-6-25
查看角色的信息
Copyright 2014 www.9miao.com
'''
import random
import operator
from datetime import datetime
from app.configdata import msgconfig
from app.configdata.globalconfig import DOMAIN, OAUTH2
from app.handler.service import serviceHandle, wservice
from app.models.role import Role, God
from app.core.charater import Charater

@serviceHandle("property")
def RoleProperty(openid,request):
    """获取获取角色属性
    """
    seqnostr = request.replace("属性", "").strip()
    try:
        seqno = int(seqnostr)
    except ValueError:
        seqno = 1
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = []
    try:
        partner = player.partners.getPartnerBySeqno(seqno)
    except IndexError:
        return {"result":True,"data":"伙伴序号有误，请重新选择"}
    partner_info = partner.attribute.getAttributeFormat()
    info.append(partner_info)
    player.plot.notice('property')#通知查看了角色的属性
    info.append("请选择操作对象：")
    for i, partner in enumerate(player.partners.getPartners(),start=1):
        info.append("%s.%s" % (i, partner.getName()))
    info.append("\n操作提示：输入名字前序号，可以查看相应人物属性信息，例如：输入“1”获得主角信息")
    weiuser.prev_command = "property"
    player.model.save()
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("formation_info")
def getFormationInfo(openid,request):
    """获取阵法信息
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = ["【当前拥有伙伴】"]
    for i, p in enumerate(player.partners.getPartners()[1:],start=1):
        info.append("%s：%s" %(i, p.getName()))
    if len(info) == 1:
        info.append("暂时没有伙伴")
    info.append("【当前阵法】")
    info.append(player.formation.getFormationInfo())
    info.append("\n操作提示：更换阵法请输入“更换阵法”，如“更换阵法 @2@3@4”，即上阵2号、3号和4号伙伴，若输入“@”则所有伙伴都不上阵")
    player.plot.notice('formation_info')#通知查看了角色的属性
    player.model.save()
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("change_formation")
def changeFormation(openid, request):
    """更换阵法
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    plist = request.split('@')
    ps = [int(p) for p in plist[1:] if p.isdigit()] 
    if not ps:
        player.formation.reset()
    else:
        try:
            ps.append(0) #加入主角
            partners = [ player.partners.getPartnerBySeqno(p+1) for p in ps]
        except IndexError:
            return {"result":True,"data":"伙伴序号有误，请重新选择"}
        player.formation.reset()
        partners.sort(key=operator.attrgetter("formationSerial"))
        for i,p in enumerate(partners,start=1):
            player.formation.setFormation(i, p.template)

    player.model.save()
    return wservice.call("formation_info",openid,request)

    

@serviceHandle("skill")
def getSkillInfo(openid, request):
    """获取技能信息
    """ 
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = []
    for i, partner in enumerate(player.partners.getPartners(),start=1):
        attr = partner.attribute.getSkillDetails()
        info.append("%s.%s" % (i, partner.getName()))
        info.append("  灵诀:{skill_1} 【{skill_1_desc}】\n  神术:{skill_2} 【{skill_2_desc}】\n".format(**attr))
    player.plot.notice("skill")
    player.model.save()
    return {"result":True,"data":"\n".join(info)}



@serviceHandle("package")
def package(openid, request):
    """背包
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    info = player.package.view() or "背包为空"
    return {"result":True,"data":info}


_FT = (("阵法", "formation_info"), ("酒馆", "tavern"))
@serviceHandle("formation_tavern")
def formation_tavern(openid, request):
    """布阵·酒馆
    """
    info = ["%s.%s" % (i, f[0]) for i,f in enumerate(_FT, start=1)]
    info.append("\n提示请输入功能序号，如1将查询”阵法“信息")
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    player.model.prev_command = "formation_tavern"
    player.model.save()
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("formation_tavern_choice")
def formation_tavern_choice(openid, request):
    try:
        return wservice.call(_FT[int(request)-1][1],openid,request)
    except (ValueError,IndexError):
        return {"result":True,"data":"功能序号有误"}


_PS = (("属性", "property"), ("技能", "skill"))
@serviceHandle("property_skill")
def property_skill(openid, request):
    """属性·技能
    """
    info = ["%s.%s" % (i, f[0]) for i,f in enumerate(_PS, start=1)]
    info.append("\n提示请输入功能序号，如1将查询”属性“信息")
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    player.model.prev_command = "property_skill"
    player.model.save()
    return {"result":True,"data":"\n".join(info)}

@serviceHandle("property_skill_choice")
def property_skill_choice(openid, request):
    try:
        return wservice.call(_PS[int(request)-1][1],openid,request)
    except (ValueError,IndexError):
        return {"result":True,"data":"功能序号有误"}
    
    

@serviceHandle("pay")
def pay(openid, request):
    """充值
    """
    return {"result":True,"data":"该功能正在开发，敬请期待！！！"}