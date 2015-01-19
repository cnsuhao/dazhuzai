#coding:utf-8
"""
Copyright 2014 www.9miao.com
"""
from django.db import models
from django.contrib import admin
# Create your models here.

class GlobalData(models.Model):
    
    fieldname = models.CharField(max_length=255,verbose_name="字段名称",unique=True)
    values = models.CharField(max_length=1024,verbose_name="全局值",null=True,blank=True)
    timestamp = models.CharField(max_length=1024,verbose_name="更新时间",null=True,blank=True)
    
    class Meta:
        verbose_name = "全局值信息"
        verbose_name_plural = "全局值信息"
        ordering = ('id','fieldname')
        
    def __unicode__(self):
        return self.fieldname
    
    
class GlobalDataAdmin(admin.ModelAdmin):
    
    list_display = ('fieldname','values','timestamp')
    search_fields = ['fieldname']
    
admin.site.register(GlobalData, GlobalDataAdmin)
    
    
    
