#coding:utf-8
'''
Created on 2014-7-21

Copyright 2014 www.9miao.com
'''
import random
import urllib2
import hashlib
import time
from gfirefly.dbentrust.util import ReadDataFromDB
import xml.etree.ElementTree as ET
import json
from urllib import quote

APPID = ""
APPKEY = ""
APPSECRET = ""
URL = ""
TOKEN = ""

MCHID = ""
KEY = ""

ACCESS_TOKEN = ""
ACCESS_TOKEN_TIMESTAMP = 0
EXPIRES_IN = 7200
ACCESS_GET_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential"
PUSH_CUSTOMER_MSG = "https://api.weixin.qq.com/cgi-bin/message/custom/send"
MONGO_HOST = "localhost:27017"#"localhost:20000,localhost:20001,localhost:20002"
MONGO_DB = "testdb"
DOMAIN = "http://www.dzzol.com"
OAUTH2 = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx0d16788ba912197a&redirect_uri=%s&response_type=code&scope=snsapi_base&state=1#wechat_redirect"

def init_global_config():
    """获取全局的配置值
    """
    global APPID,APPSECRET,URL,TOKEN,ACCESS_TOKEN,ACCESS_TOKEN_TIMESTAMP,MONGO_HOST,MONGO_DB
    resultlist = ReadDataFromDB('config_globaldata')
    global_config = {}
    for _conf in resultlist:
        global_config[_conf['fieldname']] = _conf
    if global_config.get('APPID'):
        APPID = global_config['APPID']['values']
    if global_config.get('APPSECRET'):
        APPSECRET = global_config['APPSECRET']['values']
    if global_config.get('URL'):
        URL = global_config['URL']['values']
    if global_config.get('TOKEN'):
        TOKEN = global_config['TOKEN']['values']
    if global_config.get('ACCESS_TOKEN'):
        ACCESS_TOKEN = global_config['ACCESS_TOKEN']['values']
    if global_config.get('ACCESS_TOKEN_TIMESTAMP'):
        ACCESS_TOKEN_TIMESTAMP = global_config['ACCESS_TOKEN_TIMESTAMP']['values']
    if global_config.get('MONGO_HOST'):
        MONGO_HOST = global_config['MONGO_HOST']['values']
    if global_config.get('MONGO_DB'):
        MONGO_DB = global_config['MONGO_DB']['values']
    

def get_Access_token():
    """获取access_token
    """

    global ACCESS_TOKEN,ACCESS_TOKEN_TIMESTAMP
    if not ACCESS_TOKEN_TIMESTAMP:
        ACCESS_TOKEN_TIMESTAMP = 0
    delta = time.time()-int(ACCESS_TOKEN_TIMESTAMP)
    if ACCESS_TOKEN and delta<EXPIRES_IN:
        return ACCESS_TOKEN
    url = ACCESS_GET_URL+"&appid=%s&secret=%s"%(APPID,APPSECRET)
    ACCESS_TOKEN_TIMESTAMP = time.time()
    response = urllib2.urlopen(url)
    data = json.loads(response.read())
    ACCESS_TOKEN = data.get('access_token')
    return ACCESS_TOKEN


def getOpenID(code):
    """获取openid
    """
    api = """https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"""%(APPID,APPSECRET,code)
    result = urllib2.urlopen(api).read()
    return json.loads(result)
    
    
def getUserInfo(openid):
    """获取微信用户的信息
    """
    access_token = get_Access_token()
    url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
    result = urllib2.urlopen(url).read()
    print "result:\n",result
    data = json.loads(result)
    if data.get("errcode")==40001:
        RefreshAccess_token()
        access_token = get_Access_token()
        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid)
        result = urllib2.urlopen(url).read()
        print "result:\n",result
        data = json.loads(result)
        return data
    return data








            






