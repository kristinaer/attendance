# -*- coding: utf-8 -*-
'''
Расписание
'''
from django.db import models

from users.models import User, GroupS
from schedules.models import Schedule_list
from core.models import BaseModel


TASK_STATUS = (
    ('active', 'активное'),
    ('delete', 'удаленное')
)
class Task(BaseModel):
    '''
    Задание
    '''
    title = models.CharField(
        verbose_name = u'Название',
        max_length = 254,
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    description = models.CharField(
        verbose_name = u'Описание',
        max_length = 250
    )
    teacher = models.ForeignKey(
        User,
        verbose_name = u'Преподаватель'
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name = u'Предмет'
    )
    delivery_date= models.DateTimeField(
        verbose_name = u'Дата сдачи',
        null=True, blank=True
    )
    group = models.ForeignKey(
        GroupS,
        verbose_name = u'Группа'
    )
    schedule = models.ForeignKey(
        Schedule_list,
        verbose_name=u'Расписание'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=TASK_STATUS,
        default='active'
    )

    class Meta:
        verbose_name = u'Занятие'
        verbose_name_plural = u'Занятия'


SUBJECT_STATUS = (
    ('active', 'активный'),
    ('delete', 'удаленный')
)
class Subject(BaseModel):
    '''
    Предмет
    '''
    name = models.CharField(
        verbose_name = u'Название',
        max_length = 254,
    )
    short_name = models.CharField(
        verbose_name = u'Короткое название',
        max_length = 50
    )
    description = models.CharField(
        verbose_name = u'Описание',
        max_length = 250
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=SUBJECT_STATUS,
        default='active'
    )
    class Meta:
        verbose_name = u'Предмет'
        verbose_name_plural = u'Предметы'

TASK_STATUS = (
    ('active', 'активное'),
    ('delete', 'удаленное')
)
class TaskUser(BaseModel):
    '''
    Сдача задания
    '''
    task = models.ForeignKey(
        Task,
        verbose_name = u'Задание'
    )
    user = models.ForeignKey(
        User,
        verbose_name = u'Студент'
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    date = models.DateTimeField(
        verbose_name = u'Дата'
    )
    note = models.CharField(
        verbose_name = u'Описание',
        max_length = 250
    )
    is_pass = models.BooleanField(
        verbose_name = u'Сдано',
        default=False
    )
    class Meta:
        verbose_name = u'Сдача задания'
        verbose_name_plural = u'Сдача заданий'
