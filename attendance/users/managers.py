# -*- coding: utf-8 -*-
'''
Механизмы управления пользователями для совместимости с переопределенной
моделью django.contrib.auth.models.User
https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager
'''

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    pass