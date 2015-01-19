#coding:utf-8
'''
Created on 2014-7-18

@author: root
'''
import re
import hashlib

from app.configdata.globalconfig import APPID, APPSECRET, TOKEN


def checkMD5(*args):
    """
    """
    sourcestrlist =[TOKEN,]+list(args[1:])
    sourcestrlist.sort()
    sourcestr = "".join(sourcestrlist)
    sha = hashlib.sha1(sourcestr)
    print sha.hexdigest().lower()
    return sha.hexdigest().lower()==args[0].lower()

_num = re.compile(r"(\d+)")
def getDigest(string):
    return _num.search(string).group(0)


def checkAppSignature(issubscribe,noncestr,openid,timestamp,AppSignature):
    """检测AppSignature
    """
    signature_a_str = "appid=%s&appkey=%s&issubscribe=%s&noncestr=%s&openid=%s&timestamp=%s"%(APPID,APPKEY,
                                                                issubscribe,noncestr,openid,timestamp)
    print "signature_a_str:\n",signature_a_str
    sha = hashlib.sha1(signature_a_str)
    app_signature = sha.hexdigest()
    print "app_signature:\n",app_signature
    return app_signature == AppSignature