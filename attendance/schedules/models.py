# -*- coding: utf-8 -*-
'''
Расписание
'''
from django.db import models

from users.models import User, GroupS
from studies.models import Subject
from core.models import BaseModel


SCHEDULE_STATUS = (
    ('active', 'активный'),
    ('delete', 'удаленный')
)
OSEN_VESNA_STATUS = (
    ('osen', 'Осень'),
    ('vesna', 'Весна')
)
class Schedule(BaseModel):
    '''
    Учебный год
    '''
    year = models.CharField(
        verbose_name = u'Год',
        max_length = 254,
    )
    start_date = models.DateTimeField(
        verbose_name = u'Дата начала',
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    osen_vesna = models.CharField(
        verbose_name = u'Осень/весна',
        max_length = 50,
        choices=OSEN_VESNA_STATUS,
        default='osen'
    )
    is_numerator = models.BooleanField(
        verbose_name = u'Числитель',
        default=True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=SCHEDULE_STATUS,
        default='active'
    )

    def __unicode__(self):
        return '%s %s' % (self.year, self.osen_vesna)

    class Meta:
        verbose_name = u'Учебный год'
        verbose_name_plural = u'Учебные года'


TYPE = (
    ('lecture', 'Лекция'),
    ('practice', 'Практика')
)
class Schedule_list(BaseModel):
    '''
    Расписание
    '''
    weekday = models.IntegerField(
        verbose_name=u'День недели'
    )
    is_numerator = models.BooleanField(
        verbose_name = u'Числитель',
        default=True,
        null=True, blank=True
    )
    teacher = models.ForeignKey(
        User,
        verbose_name=u'Преподаватель'
    )
    number_pairs = models.IntegerField(
        verbose_name = u'Номер пары'
    )
    type = models.CharField(
        verbose_name = u'Тип',
        max_length = 50,
        choices=TYPE,
        default='lecture'
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name=u'Предмет'
    )
    group = models.ForeignKey(
        GroupS,
        verbose_name=u'Группа'
    )
    schedule = models.ForeignKey(
        Schedule,
        verbose_name=u'Учебный год'
    )

    class Meta:
        verbose_name = u'Расписание'
        verbose_name_plural = u'Расписание'


LESSON_STATUS = (
    ('delete', 'отменен'),
    ('replace', 'перенесен')
    ('standart', 'обычно')
)
class Lesson(BaseModel):
    '''
    Занятие
    '''
    schedule_list = models.ForeignKey(
        Schedule_list,
        verbose_name=u'РАсписание'
    )
    date = models.DateTimeField(
        verbose_name = u'Дата занятия'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=LESSON_STATUS,
        default='standart'
    )

    class Meta:
        verbose_name = u'Занятие'
        verbose_name_plural = u'Занятия'


STATUS_PRESENT = (
    ('present', 'Присутствует'),
    ('missing', 'Отсутствует')
    ('was_late', 'Опоздал')
)
class LessonStudents(BaseModel):
    '''
    Студенты группы
    '''
    user = models.ForeignKey(
        User,
        verbose_name = u'Студент',
    )
    lesson = models.ForeignKey(
        Lesson,
        verbose_name = u'Занятие',
    )
    status_present = models.BooleanField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS_PRESENT,
        default='present'
    )
    note = models.DateTimeField(
        verbose_name = u'Примечание',
        null=True, blank=True
    )

    class Meta:
        verbose_name = u'Присуствие Студента'
        verbose_name_plural = u'Присуствие Студентов'
