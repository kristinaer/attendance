# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.paginator import Paginator, InvalidPage


class Pager(object):
    '''
    Обертка упрощающая использование django Paginator (постраничный вывод списка объектов)
    '''
    def __init__(self, settings_section='', **kwargs):
        """
        :param settings_section: Блок настроек, который нужно взять из глобальных настроек
                                 например settings_section='info' возьмет settings.PAGINATOR.info
                                 если такого блока настроек нет, то будут взяты дефолтные
        """
        sp = settings.PAGINATOR
        self.cfg = sp.get(settings_section, sp.get("default"))
        self.cfg.update(kwargs)

    def get(self, qs, page_num):
        """
        Собственно данные лимитированные пейджингом а также мета информация для постороения UI пейджинга
        :param qs: QuerySet instance
        :param page_num: Номер страницы, для которой нужно получить данные
        :return: Словарь:
                objects_list - список объектов для данной страницы
                сount        - количество объектов
                pages        - список номеров страниц (не более десяти по пять слема и справа от текущей страницы)
                next_page    - номер следующей страницы или ноль если нет следующей
                prev_page    - номер предыдующей страницы или ноль если нет предыдующей
                cur_page     - номер текущей страницы
                count_page   - количество страниц
        """
        per_page = self.cfg.get("per_page")
        paginator = Paginator(qs, per_page)
        try:
            pageObj = paginator.page(page_num)
        except InvalidPage:
            pageObj = paginator.page(1)
            page_num = 1

        p = int(page_num)
        pages = []
        for i in paginator.page_range:
            pages.append({
                'page_num': i,
                'is_active': (p == i)
            })
        ret = {
            'objects_list': pageObj.object_list if pageObj else [],
            'count': paginator.count,
            'pages': pages[p - 5 if p >= 5 else 0 : p + 4 if p > 5 else 9],
            'next_page': p + 1 if p < paginator.num_pages else 0,
            'prev_page': p - 1 if p > 1 else 0,
            'cur_page': p,
            'count_page': paginator.num_pages,
        }
        return ret
