#coding:utf8
'''
Created on 2014-6-18

Copyright 2014 www.9miao.com
'''
from gtwisted.utils import log

class WeiWuXiaService():
    
    def __init__(self):
        """
        """
        self.targets = {}
    
    def mapTarget(self,funckey,func):
        """
        """
        assert not self.targets.has_key(funckey)
        self.targets[funckey] = func
        
    def unMapTarget(self,funckey,func):
        """
        """
        assert self.targets.has_key(funckey)
        del self.targets[funckey]
        
    def call(self,funckey,*args,**kw):
        """
        """
        from app.ability.pushmsg import PushActionMessage
        log.msg("call method [%s] from service "%funckey)
        assert self.targets.has_key(funckey)
        response = self.targets[funckey](*args,**kw)
        PushActionMessage(args[0])
        response["data"] = response.get("data","")
        return response
    

wservice = WeiWuXiaService()


class serviceHandle:
    
    def __init__(self,funckey):
        self.funckey = funckey
        
    def __call__(self,func):
        """
        """
        wservice.mapTarget(self.funckey, func)

    
    
        
        
        
        