#coding=utf8
from django.db import models
from django.forms import ModelForm
from helpers import get_models_cfg

typemap = {'int':'IntegerField', 'char': 'CharField', 'date': 'DateField'}

doc = get_models_cfg()
for mod in doc.keys():
    field_dict = {
        '__module__': __name__,
        'id': models.AutoField(primary_key=True) 
    }
    for yfield in doc[mod]['fields']:             
        field_dict[yfield['id']] = getattr(models, typemap[yfield['type']])(yfield['title'], max_length=64)
    mod_cls = mod.capitalize()
    form_cls = "{0}Form".format(mod_cls)
    globals()[mod_cls] = type(mod_cls, (models.Model,), field_dict) 
    globals()[form_cls] = type(form_cls, (ModelForm,), {'Meta': type('Meta', (object,), {'model': globals()[mod_cls], 'fields': '__all__'})})

