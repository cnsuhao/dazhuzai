#coding:utf8
'''
Created on 2014-6-18

@author: root
'''
import urllib2,cookielib 
import time

def produceTextMsg(openid,Content):
    """
    """
    CreateTime = int(time.time())
    formatXml = """
        <xml>
        <ToUserName><![CDATA[ToUserName]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>"%s"</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        </xml>
        """%(openid,CreateTime,Content)
        
    return formatXml

def produceEventMsg(openid,event):
    """
    """
    CreateTime = int(time.time())
    formatXml = """<xml>
        <ToUserName><![CDATA[ToUserName]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[event]]></MsgType>
        <Event><![CDATA[%s]]></Event>
        </xml>"""%(openid,CreateTime,event)
    return formatXml


def post3():   
# for mail.sina.com.cn

    cj = cookielib.CookieJar() 
    url_login = 'http://localhost:8000/do?signature=e8da62e6be35961f5d351d7ffc058f4483f062ad&timestamp=1403086030&nonce=570842442' 
    body = (('logintype','login'), ('u','username'), 
        ('psw', '********'))
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
    #opener.addheaders = [('User-agent', 'Opera/9.23')] 
    opener.addheaders = [('User-agent', 
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
    urllib2.install_opener(opener) 
    req=urllib2.Request(url_login,produceTextMsg("123","123","123")) 
    u=urllib2.urlopen(req)
    print u.read().decode('utf-8').encode('gbk')
    
    


url_login = 'http://localhost:9000/do?signature=e8da62e6be35961f5d351d7ffc058f4483f062ad&timestamp=1403086030&nonce=570842442'

class WeixinClient:
    """微信客户端模拟
    """
    
    def __init__(self,openid):
        """
        """
        self.url = url_login
        self.openid = openid
        
    def post(self,request):
        """
        """
        cj = cookielib.CookieJar() 
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj)) 
        #opener.addheaders = [('User-agent', 'Opera/9.23')] 
        opener.addheaders = [('User-agent', 
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        urllib2.install_opener(opener) 
        req=urllib2.Request(url_login,request) 
        u=urllib2.urlopen(req)
        return u.read()
        
    def subscribe(self):
        """微信关注
        """
        request = produceEventMsg(self.openid, "subscribe")
        response = self.post(request)
        return response
    
    def unsubscribe(self):
        """微信关注
        """
        request = produceEventMsg(self.openid, "unsubscribe")
        response = self.post(request)
        return response
        
    def message(self,content):
        """
        """
        request = produceTextMsg(self.openid, content)
        response = self.post(request)
        return response
        
        
if __name__ == '__main__':
    
    user = WeixinClient("apspsp")
#     print user.subscribe()
    print user.message("战斗")







