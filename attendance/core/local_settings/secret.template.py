# -*- coding: utf-8 -*-

# Закрывающие определения (в конце settings.py).
# Полностью переопределяют определения в local.py и settings.py

from core.local_settings.local import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'attendance',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

EMAIL_PORT = 25
EMAIL_HOST_USER = 'kristinaer14@mail.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True


MAILER_PORT = EMAIL_PORT
MAILER_USER = EMAIL_HOST_USER
MAILER_PASSWORD = EMAIL_HOST_PASSWORD
MAILER_USE_TLS = EMAIL_USE_TLS

MAILER_SALT = ['']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

BITLY = {
    'login': '',
    'api_key': ''
}

SERVER_EMAIL = EMAIL_HOST_USER
