# -*- coding: utf-8 -*-
'''
Общие для всех моделей атрибуты и общие модели
'''

from django.db import models
from django.contrib.contenttypes.models import ContentType



class AttendanceMixins(object):
    '''
    Класс для расширений всех внутренних моделей
    '''
    def get_object_name(self):
        '''
        Уникальное на уровне проекта название модели
        '''
        return ('%s_%s' % (self._meta.app_label, self._meta.object_name)).lower()

    def get_app(self):
        return self._meta.app_label

    def get_content_type(self):
        try:
            return ContentType.objects.get_for_model(self)
        except ContentType.DoesNotExist:
            return None


class BaseModel(models.Model, AttendanceMixins):
    '''
    Базовый классс для всех внутренних моделей
    Внимание! Все расширения должны быть реализованы в AttendanceMixins
    иначе они не будут учтены как минимум в модели users.User
    '''
    class Meta:
        abstract = True
