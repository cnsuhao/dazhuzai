#coding:utf-8
import os
import csv
import re
import json
import traceback
from django.core.management.base import BaseCommand, CommandError
from wuxia_admin.gamedata.models import *


SINGLE = re.compile(r"\s*//.*$",re.M)
MULTI = re.compile(r"\s*/\*.*?\*/",re.S)
def strip_comment(config):
    for pattern in (SINGLE, MULTI):
        config = pattern.sub("", config)
    return config

class DataCenter(object):
    def __init__(self, config, debug):
        self.config = config
        self.debug = debug
        self.rootpath = config.get("rootpath")
        self.decode = config.get("decode")
        self.encode = config.get("encode")
        self.separator = config.get("separator")
        assert os.path.isdir(self.rootpath)
        self.models = self.import_app(config.get("app"))

    def import_app(self, appname):
        from django.db.models.loading import get_app 
        return get_app(appname)

    def start(self):
        for model in self.config.get("models"):
            print "process model %s start" % model
            try:
                self.do_model(model)
            except:
                print traceback.format_exc()
            else:
                print "success!!!!!!!!!!"
            finally:
                print "process model %s end" % model
       
    def do_model(self, modelname):
        model = getattr(self.models, modelname)
        modelconfig = self.config["models"][modelname]
        mode = modelconfig.get("mode") or "w"
        filename = "gamedata_" + modelname.lower() + '.csv'
        filename = os.path.join(self.rootpath,filename)
        if not os.path.isfile(filename):
            print "no file:%s exist" % filename
            return
        else:
            fileobj = open(filename,"r")
        reader=csv.reader(open(filename,'rb'),delimiter='\t')
        field_dict = dict([(i,f) for i,f in enumerate(reader.next()[1:],start=1)])
        print field_dict
        if self.debug:
            print 'please check field and heads,return'
            return
        if mode == "w":
            model.objects.all().delete()
        for fs in reader:
            record = {}
            for i,f in field_dict.iteritems():
                try:
                    record[f] = fs[i].decode(self.decode).encode(self.encode)
                    #record[f] = fs[i]
                except IndexError,e:
                    record[f] = 0
            try:
                m = model(**record)
                m.save()
            except Exception,e:
                print "record exception:%s,record,%s" % (str(record),str(e))

class Command(BaseCommand):
     def handle(self, *args, **options):
        with open(args[0],'r') as f:
            config = strip_comment(f.read())
            debug = False
            if len(args) == 2:
                debug = True
            data = DataCenter(json.loads(config),debug)
            data.start()
