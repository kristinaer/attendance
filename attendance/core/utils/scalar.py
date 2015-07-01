# -*- coding: utf8 -*-
'''
Функции для работы с числами и строками
'''

def is_string(s):
    if isinstance(s, str) or isinstance(s, unicode):
    # вроде как обычно делают так:
    #if isinstance(s, basestring):
        return True
    return False
