#coding=utf8
from django.test import TestCase, RequestFactory
from django.shortcuts import get_object_or_404
from helpers import get_models_cfg
import models
import unittest
import types

class ModelsConfigCase(TestCase):
    def test_models_cfg_type(self):
        self.assertEqual(type(get_models_cfg()), dict)
    
class ModelsClassesCase(TestCase):

    def setUp(self):
        self.field_values = {
            'char': 'hello',
            'int': 123,
            'date': '2001-10-01'
        }
        self.doc = get_models_cfg()
    
    def test_model_create(self):
        for model_id in self.doc.keys():
            model_cls_name = model_id.capitalize()
            form_cls_name = "{0}Form".format(model_cls_name) 
            model_cls = getattr(models, model_cls_name)
            form_cls = getattr(models, form_cls_name)

            self.assertTrue(type(model_cls), types.ClassType)
            self.assertTrue(type(form_cls), types.ClassType)

            kw = {}
            for field in self.doc[model_id]['fields']:  
                kw[field['id']] = self.field_values[field['type']]
            model_obj = model_cls(**kw)

            self.assertIsInstance(model_obj, model_cls)

class ViewsTestsCase(TestCase):
    
    def setUp(self):
        self.field_values = {
            'char': 'hello',
            'int': 123,
            'date': '2001-10-01'
        }
        self.doc = get_models_cfg()

    def test_index_get(self):
        resp = self.client.get('/') 
        self.assertEqual(resp.status_code, 200)
        
    def test_json_cls_get(self):
        resp = self.client.get('/json_cls/') 
        self.assertEqual(resp.status_code, 200)
        
    def test_json_obj_get(self):
        for model_id in self.doc.keys():
            resp = self.client.get('/json_obj/{0}/'.format(model_id)) 
            self.assertEqual(resp.status_code, 200)

    def test_obj_create_post(self):
        for model_id in self.doc.keys():
            params = {}
            for field in self.doc[model_id]['fields']:  
                params[field['id']] = self.field_values[field['type']]
            resp = self.client.post('/obj_create/{0}/'.format(model_id), params)
            self.assertEqual(resp.status_code, 200)

    def test_obj_update_post(self):
        new_field_val = {
            'char': 'qwe',
            'int': 235,
            'date': '1999-12-04'
        }
        for model_id in self.doc.keys():
            model_cls_name = model_id.capitalize()
            model_cls = getattr(models, model_cls_name)
            kw = {}
            for field in self.doc[model_id]['fields']:  
                kw[field['id']] = self.field_values[field['type']]
            model_obj = model_cls(**kw)
            model_obj.save()

            for field in self.doc[model_id]['fields']:  
                params = {
                    'objid': model_obj.id,
                    'field': field['id'],
                    'value': new_field_val[field['type']]
                }
                resp = self.client.post('/obj_update/{0}/'.format(model_id), params)
                self.assertEqual(resp.status_code, 200)
                model_obj = get_object_or_404(model_cls, id=model_obj.id)
                field_val = getattr(model_obj, field['id'])
                if field['type'] == 'date': field_val = field_val.strftime('%Y-%m-%d')
                self.assertEqual(field_val, new_field_val[field['type']])












