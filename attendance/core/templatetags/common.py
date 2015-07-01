# -*- coding: utf-8 -*-

import datetime
import json
import math
import pytils
from random import choice as rchoice

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django import template
from django.conf import settings

from core.utils.url import modify_url as modify_url_
from core.utils.scalar import is_string


register = template.Library()

@register.filter
def get(dict_, key):
    '''
    Получение из словаря (или dict-like объекта) значения под переданным ключом
    Если значение пустое или данные невозможно получить возвращается пустая строка
    Пример {{ my_dict|get:'my_key' }}
    '''
    if not is_string(key):
        try:
            key = str(key)
        except UnicodeEncodeError:
            key = unicode(key)
    return dict_.get(key, u'') if hasattr(dict_, 'get') and callable(dict_.get) else u''

@register.simple_tag(takes_context=True)
def modify_url(context, operation, *params):
    '''
    Враппер для функций модуля urlobject
    https://urlobject.readthedocs.org/en/latest/quickstart.html
    Назначение: разобрать текщий URL, поменять какую-то его часть и вернуть модифицированный URL в виде строки
    Например: {% modify_url 'del_query_param' 'page' %} уберет пейджинг из запроса
    Возвращает URL без домена
    '''
    request = context.get('request')
    if not request:
        return u''
    current_url = request.get_full_path()
    return modify_url_(current_url, operation, *params)

@register.simple_tag()
def selected(option_value, user_input_value):
    '''
    Сокращение для установки текущего элемента в списке <select>
    Например
    <option value="{{ data.id }}" {% selected data.id request.GET.data_id %}></option>
    '''
    return u'selected="selected"' if unicode(option_value) == unicode(user_input_value) else u''

@register.simple_tag()
def checked(user_input_value):
    '''
    Сокращение для установки текущего элемента в списке <select>
    Например
    <input type="checkbox" value="{{ data.id }}" {% checked request.GET.data_id %}></option>
    '''
    return u'checked="checked"' if unicode(user_input_value).strip() else u''

@register.simple_tag()
def rssdate(date=None, default=None):
    '''
    Получение даты в формате удобном для вывода в rss лентах
    Wed, 03 Jul 2013 11:07:06
    '''
    if not date and default:
        date = default
    elif not date:
        date = datetime.datetime.now()
    return date.strftime('%a, %d %b %Y %H:%M:%S +0600')

@register.filter(name='chunks')
def chunks(iterable, chunk_size):
    '''
    Разбивает итерируемые данные, например список на блоки указанных размеров
    Например если d = [1,2,3,1,2,3] то d|chunks:3 вернет [[1,2,3], [1,2,3]]
    '''
    if not hasattr(iterable, '__iter__'):
        # can't use "return" and "yield" in the same function
        yield iterable
    else:
        i = 0
        chunk = []
        for item in iterable:
            chunk.append(item)
            i += 1
            if not i % chunk_size:
                yield chunk
                chunk = []
        if chunk:
            # some items will remain which haven't been yielded yet,
            # unless len(iterable) is divisible by chunk_size
            yield chunk

@register.filter
def columns(iterable, columns_count):
    if not columns_count or columns_count == 1:
        return iterable
    l = len(iterable)
    colsize = int(math.ceil(float(l)/float(columns_count)))
    columned = []
    for i in range(0, columns_count):
        columned.append(iterable[i*colsize:(i+1)*colsize])
    return columned

@register.filter
def human_date(for_date):
    n = datetime.datetime.now().replace(hour=23, minute=59)
    c = pytils.dt.distance_of_time_in_words(for_date)
    ts = (n - for_date).total_seconds()

    SECONDS_IN_DAY = 86400

    if SECONDS_IN_DAY < ts < SECONDS_IN_DAY*2:
        return u'вчера %s' % for_date.strftime('%H:%M')

    if SECONDS_IN_DAY*2 < ts < SECONDS_IN_DAY*3:
        return u'позавчера %s' % for_date.strftime('%H:%M')

    return pytils.dt.ru_strftime(u'%d %b %H:%M', for_date, inflected=True).lstrip('0')

@register.filter()
def human_size(bytes):
    steps = [u'B', u'Кб', u'Мб', u'Гб', u'Тб', u'Пб']
    idx = 0
    bytes = float(bytes)
    while bytes > 1024:
        bytes /= 1024
        if idx < len(steps):
            idx += 1
    return u'%s %s' % (
        ('%.2f' % bytes).rstrip('.0'),
        steps[idx],
    )

@register.tag
def capture(parser, token):
    """{% capture as [foo] %}"""
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'capture' node requires `as (variable name)`.")
    nodelist = parser.parse(('endcapture',))
    parser.delete_first_token()
    return CaptureNode(nodelist, bits[2])


class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = mark_safe(output.strip())
        return ''


@register.simple_tag()
def number_format(number, decimals=0, dec_point='.', thousands_sep=','):
    '''
    Аналог фильтра Twig number_format
    Дистрибутирован из джанго сниппетов http://djangosnippets.org/snippets/682/
    Документация http://twig.sensiolabs.org/doc/filters/number_format.html
    '''
    try:
        number = round(float(number), decimals)
    except ValueError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []

    parts.extend([integer[m+t:m+t+3] for t in xrange(0, len(integer[m:]), 3)])

    if decimals:
        return '%s%s%s%s' % (
            neg and '-' or '',
            thousands_sep.join(parts),
            dec_point,
            fractional.ljust(decimals, '0')[:decimals]
        )
    else:
        return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

@register.filter()
def prettify_json(json_data):
    json_data = json.dumps(json.loads(json_data), indent=4, ensure_ascii=False)
    return json_data


@register.filter()
def indent_text(text, indent_by='\t'):
    '''
    Делает отступ у каждой строки в text заданным набором символов indent_by
    '''
    text = text.replace('\n\r', '\n').replace('\r\n', '\n')
    text = text.replace('\n', '\n%s' % indent_by)
    return '%s%s' % (indent_by, text)
