#coding:utf8
'''
Created on 2014-8-26

Copyright 2014 www.9miao.com
'''

from app.handler.service import serviceHandle
from app.models.role import Role, Friendship
from app.core.charater import Charater
from app.configdata import gamedataconfig
from app.utils.hashtools import getDigest

@serviceHandle('tavern')
def tavern(openid, request):
    """酒馆
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    partner_info = gamedataconfig.ALL_PARTNER_INFO
    partner_ids = [partner_id for partner_id in partner_info.iterkeys() if not player.partners.checkHasPartner(partner_id) ]
    friendships = dict(((f.partner_id, f.friendship) for f in player.model.friendships))
    info = ["%s. %s (交情值：%s/%s)"  %(i, partner_info[p]["partner_name"], friendships.get(p,0), partner_info[p]["friendship"])  for i, p in enumerate(partner_ids,start=1)]
    if info:
        info.append("\n提示：输入伙伴名前的“数字”可查看对应伙伴信息")
        player.model.prev_command = "tavern"
        player.plot.notice("tavern")
        player.model.save()
    else:
        info.append("没有可招募伙伴")
   
    return {"result":True,"data":"\n".join(info)}


@serviceHandle('partnerinfo')
def partnerinfo(openid, request):
    """伙伴基础信息
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    partner_info = gamedataconfig.ALL_PARTNER_INFO
    partner_ids = [partner_id for partner_id in partner_info.iterkeys() if not player.partners.checkHasPartner(partner_id) ]
    try:
        partnerid = partner_ids[int(request)-1]
    except (ValueError,IndexError):
        return {"result":True,"data":"伙伴序号有误"}
    print 'partnerid',partnerid
    player.model.prev_command = "tavern_recruit"
    player.model.prev_objectid = partnerid
    friendships = dict(((f.partner_id, f.friendship) for f in player.model.friendships))
    attr = dict(gamedataconfig.ALL_PARTNER_INFO[partnerid]) #make a copy
    #已经有的交情
    attr["a_friendship"] = friendships[partnerid] if partnerid in friendships else 0
    skill_1 = attr.get("skill_1","90000")
    skill_2 = attr.get("skill_2","90000")
    attr["skill_1"] = gamedataconfig.ALL_SKILL_INFO[skill_1]["skill_name"]
    attr["skill_1_desc"] = gamedataconfig.ALL_SKILL_INFO[skill_1]["skill_desc"]
    attr["skill_2"] = gamedataconfig.ALL_SKILL_INFO[skill_2]["skill_name"]
    attr["skill_2_desc"] = gamedataconfig.ALL_SKILL_INFO[skill_2]["skill_desc"]
    format_info = "{partner_name} (交情：{a_friendship}/{friendship})\n气血:{maxhp}\n普通攻击:{attack}\n法术攻击:{magic_attack}\n普通防御:{defend}\n法术防御:{magic_defend}\n命中:{hit}\n闪避:{dodge}\n暴击:{crit}\n韧性:{tenacity}\n致命:{fatal}\n速度:{speed}\n灵诀:{skill_1}【{skill_1_desc}】\n神术:{skill_2}【{skill_2_desc}】"
    info = format_info.format(**attr)
    info += "\n\n提示：1.输入“增加交情”后可增加交情操作；2.输入“返回酒馆”返回到酒馆"
    player.model.save()
    return {"result":True,"data":info}

@serviceHandle('friendshipmaterial')
def friendshipmaterial(openid, request):
    """获取增加交情物品
    """
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    materials = dict(((m.materialid, m.amount) for m in player.model.materials if m.amount>0))
    #friendshipMaterials = gamedataconfig.ALL_FRIENDSHIP_CONFIG
    templates = gamedataconfig.ALL_TEMPLATE_INFO
    info = ["%s. %s(共%s个，每个可增加%s交情点)" %(i, templates[mid]["name"], materials[mid], templates[mid]["friendship"] ) for i, mid in enumerate(materials.iterkeys(), start=1) if templates[mid]["friendship"]>0 ]
    if info:
        info.append("\n提示：1.输入物品名+使用个数，即可增加交情值，例如：宝玉 3 2.输入“返回酒馆”返回到酒馆")
        player.model.prev_command = "friendshipmaterial"
    else:
        info.append("还没有可增加交情物品")

    player.model.save()
    return {"result":True,"data":"\n".join(info)}

@serviceHandle('addfriendship')
def addfriendship(openid, request):
    """增加交情
    """
    try:
        mount = getDigest(request)
        name = request.replace(mount, '').strip()
        mount = int(mount)
    except AttributeError:
        return {"result":True,"data":"格式有误，输入物品名+使用个数，例如：宝玉 3"}

    #通过物品表获取物品id
    templates = gamedataconfig.ALL_TEMPLATE_INFO
    for tid, t in templates.iteritems():
        if t["name"] == name:
            templateid = tid
            if t["friendship"] <= 0:
                return {"result":True,"data":"%s没有增加交情功能" % name}
            break
    else:
        return {"result":True,"data":"不存在该物品"}

    #根据物品id判断用户是否有该材料
    weiuser = Role.objects.get(openid=openid)
    player = Charater(weiuser)
    print templateid
    for m in player.model.materials:
        if m.materialid == templateid:
            if m.amount >= mount:
                m.amount -= mount
                break
            else:
                return {"result":True,"data":"物品数量不足"}
    else:
        return {"result":True,"data":"你没有该物品"}

    friends = templates[templateid]["friendship"] * mount
    partner_id = player.model.prev_objectid

    #对伙伴增加交情
    for f in player.model.friendships:
        if f.partner_id == partner_id:
            f.friendship += friends
            break
    else:
        f = Friendship(partner_id=partner_id, friendship=friends)
        player.model.friendships.append(f)

    need = gamedataconfig.ALL_PARTNER_INFO[partner_id]["friendship"]
    name = gamedataconfig.ALL_PARTNER_INFO[partner_id]["partner_name"]
    info = ["恭喜你，你与%s交情增加%s，当前交情值（%s/%s）" %(name, friends, f.friendship, need)]
    if f.friendship >= need:
        player.partners.AddPartner(partner_id)
        info.append("招募伙伴成功！！！\n提示：输入“返回酒馆”返回酒馆")
    else:
        info.append("\n提示：1.输入“继续增加”返回交情道具列表，会显示最新的剩余道具列表信息 2.输入“返回酒馆”返回酒馆")

    player.model.prev_command = "addfriendship"
    player.model.save()

    return {"result":True,"data":"\n".join(info)}







