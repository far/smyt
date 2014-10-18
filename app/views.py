#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core import serializers
from django.http import Http404
from django.shortcuts import get_object_or_404, render_to_response
import yaml
import json
import sys
import models
from helpers import get_models_cfg

def obj_create(request, mod_id=None):
    """
    Создание нового объекта модели
    """
    if mod_id: form_cls_name = "{0}Form".format(mod_id.capitalize())
    else: raise Http404

    # проверка существование класса формы модели в модуле моделей
    if request.POST and hasattr(models, form_cls_name):
        form_cls = getattr(models, form_cls_name)
        # создание нового объекта 
        form = form_cls(request.POST)
        obj = form.save()
        return HttpResponse(json.dumps(obj.id), content_type="application/json")
    else:
        raise Http404

def obj_update(request, mod_id=None):
    """
    Обновление поля модели POST запросом
    """
    if mod_id: model = mod_id.capitalize()
    else: raise Http404

    # проверка существование класса модели в модуле моделей
    if request.POST and hasattr(models, model):
        try:
            # определение значений для обновления модели из POST словаря
            obj_cls = getattr(models, model)
            pk      = request.POST['objid']
            field   = request.POST['field']
            value   = request.POST['value']
            # выборка объекта по ключу 
            obj = get_object_or_404(obj_cls, id=pk)
            # обновление поля объекта 
            setattr(obj, field, value)
            obj.save()
            return HttpResponse(json.dumps('ok'), content_type="application/json")
        except:
            raise Http404  
    else:
        raise Http404  

def json_obj(request, mod_id=None):
    """
    Выборка списка объектов модели в JSON формате
    """
    if mod_id: model = mod_id.capitalize()
    else: raise Http404

    # проверка существование класса модели в модуле моделей
    if hasattr(models, model):  
        form_cls = getattr(models, "{0}Form".format(model)) 
        obj_cls = getattr(models, model)
    else:
        raise Http404
    return HttpResponse(serializers.serialize('json', obj_cls.objects.all()), content_type="application/json")

def json_cls(request):
    """
    Выборка конфигурации моделей в JSON формате
    """
    return HttpResponse(json.dumps(get_models_cfg()), content_type="application/json")

def index(request):
    """
    Главная страница с списком моделей
    """
    return render_to_response('index.tmpl', {'maxint': sys.maxint}, context_instance=RequestContext(request))

