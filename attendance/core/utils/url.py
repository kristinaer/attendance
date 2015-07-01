# -*- coding: utf8 -*-
'''
Функциии работающии над преобразованием, формированием, разбором URL
А также использующие объект request
'''
import urlparse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from urlobject import URLObject
from django.core.urlresolvers import Resolver404, resolve


def redirect_with_message(request, to, message, **kwargs):
    '''
    Делает редирект на заданную страницу с прикреплением
    текстового сообщения через messages framework
    '''
    if message:
        messages.add_message(request, messages.ERROR, message)
    return redirect(to, **kwargs)


def modify_url(url, operation, *args):
    '''
    Враппер для функций модуля urlobject
    https://urlobject.readthedocs.org/en/latest/quickstart.html
    Назначение: разобрать текщий URL, поменять какую-то его часть и вернуть модифицированный URL в виде строки
    Например: {% modify_url 'del_query_param' 'page' %} уберет пейджинг из запроса
    Возвращает URL без домена
    '''
    if not operation:
        return url

    url = URLObject(url)
    op = getattr(url, operation, None)
    if callable(op):
        return unicode(op(*args))
    raise Exception('%s is incorrect function name for urlobject.URLObject' % operation)


def get_referer(request, default='/'):
    '''
    Возвращает реферер не ссылающийся на текущую страницу
    '''
    original_referer = request.META.get('HTTP_REFERER')

    if not original_referer:
        return default

    url = URLObject(original_referer)

    # Проверяем нашего ли сайта домен
    host = '.%s' % url.hostname
    if url and not host.endswith('.%s' % settings.LOCAL.get('domain')):
        return default

    current_url = URLObject(request.get_full_path())

    # Проверяем не с этой же ли самой страницы реферер
    if url.path.strip('/') == current_url.path.strip('/'):
        return default
    return original_referer


def safe_resolve(url):
    '''
    Не выбрасывающий исключение резолв url в правило роутинга
    '''
    try:
        match = resolve(url)
    except Resolver404:
        return None
    return match


def extract_company_subdomain(url):
    base_domain = settings.LOCAL.get('domain')
    hostname = urlparse.urlparse(url).hostname
    remaining = hostname[0:-(len(base_domain)+1)]
    subdomain = remaining.split('.')[-1]
    return subdomain

def get_clean_path(request):
    path = request.path

    url = request.build_absolute_uri()
    subdomain = extract_company_subdomain(url)

    if subdomain == 'news':
        path = u'/%s%s' % ('info', path)
    elif subdomain and subdomain != 'www':
        path = u'/%s%s' % (subdomain, path)

    return path
