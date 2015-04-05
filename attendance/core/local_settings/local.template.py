# -*- coding: utf-8 -*-
# Открывающие определения (в начале settings.py).
# Не должно быть этих определений в settings.py и secret.py
# иначе они переопределятся

ENABLE_DEBUG_TOOLBAR = False
DEBUG = False
TEMPLATE_DEBUG = False
SEND_BROKEN_LINK_EMAILS = True
GOOGLE_ANALYTICS_ENABLE = True
LOCAL = {
    'static_production'   : True,
    'domain'              : 'localhost', #
    'session_cookie_name' : 'session', #
    'disable_counters'    : False,
    'disable_banners'     : False,
    'disable_partners'    : False,
    'media_version'       : 0,
    'disable_traffic_informer_requests' : True,
}
