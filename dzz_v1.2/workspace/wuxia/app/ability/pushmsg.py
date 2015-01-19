#coding:utf8
'''
Created on 2014-6-18
用户推送消息
Copyright 2014 www.9miao.com
'''
import urllib,json
import time
from app.configdata import globalconfig

def produceResponsedMsg(ToUserName,FromUserName,Content):
    """被动回复微信消息
    """
    if not Content:
        return ""
    CreateTime = int(time.time())
    formatXml = """
        <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>"%s"</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>
        """%(ToUserName,FromUserName,CreateTime,Content)
    return formatXml
        
        
def pushWeixinMessage(ToUserName,Content):
    """主动推送客服消息
    """
    print "pushWeixinMessage"
    print "type(Content)",type(Content)
    access_token = globalconfig.get_Access_token()
    url = globalconfig.PUSH_CUSTOMER_MSG+"?access_token=%s"%access_token
    msg = Content
    data = {"msgtype": "text", "touser": ToUserName, "text": {"content": msg}}
    ss = json.dumps(data,ensure_ascii=False)
    result = urllib.urlopen(url, str(ss)).read()
    return result
    
    
def popROleMessage(openid):
    """推送角色的触发消息
    """
    from gtwisted.core import reactor
    from app.models.role import Role
    try:
        role = Role.objects.get(openid=openid)
    except:
        return
    messages = list(role.message)
    for msg in messages:
        pushWeixinMessage(role.openid,msg)
#         #表示推送成功
#         if not result.get("errcode"):
#             print "success"
    role.message=[]
    role.save()
    
def PushActionMessage(openid):
    from gtwisted.core import reactor
    reactor.callLater(0.1, popROleMessage,openid)
    

def produceNewsResponsedMsg(**kw):
    """图文消息
    """
    kw.setdefault("CreateTime", int(time.time()))
    kw.setdefault("ArticleCount", 1)
    count = kw.get("ArticleCount")    
    item = """
        <item>
        <Title><![CDATA[{%s}]]></Title>
        <Description><![CDATA[{%s}]]></Description>
        <PicUrl><![CDATA[{%s}]]></PicUrl>
        <Url><![CDATA[{%s}]]></Url>
        </item>"""
    keys = ("Title", "Description", "PicUrl", "Url")
    if count == 1:
        items = item % keys
    else:
        items = "".join([ item % tuple((key+str(i+1) for key in keys)) for i in xrange(count)])
    kw["Items"] = items.format(**kw)
        
    formatXml = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>{ArticleCount}</ArticleCount>
        <Articles>
        {Items}
        </Articles>
        </xml>
        """.format(**kw)
    return formatXml
    
