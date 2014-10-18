#coding=utf8
from django.contrib import admin
from models import *
from helpers import get_models_cfg

doc = get_models_cfg()
for ymodel in doc.keys():
    mod_cls = ymodel.capitalize()
    adm_cls = '{0}Admin'.format(mod_cls,)
    globals()[adm_cls] = type(adm_cls, (admin.ModelAdmin,), {})
    admin.site.register(globals()[mod_cls], globals()[adm_cls])

