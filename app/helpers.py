#coding=utf8
import yaml
from smytapp.settings import MODELS_CFG 

def get_models_cfg(path=MODELS_CFG):
    """
    Чтение файла конфигурации моделей 
    """
    doc = None
    try:
        with open(path, 'r') as f:
            doc = yaml.load(f)
    except:
        raise Exception('Ошибка чтения файла конфигурации моделей')
    else:
        return doc

