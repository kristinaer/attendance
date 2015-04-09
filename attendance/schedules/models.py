# -*- coding: utf-8 -*-
'''
Расписание
'''
from django.db import models

from users.models import User, GroupSt
from core.models import BaseModel


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
        default=SUBJECT_STATUS[0][0]
    )
    class Meta:
        verbose_name = u'Предмет'
        verbose_name_plural = u'Предметы'


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
        default=OSEN_VESNA_STATUS[0][0]
    )
    is_numerator = models.BooleanField(
        verbose_name = u'Числитель',
        default=True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=SCHEDULE_STATUS,
        default=SCHEDULE_STATUS[0][0]
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
class ScheduleList(BaseModel):
    '''
    Расписание
    '''
    weekday = models.IntegerField(
        verbose_name=u'День недели'
    )
    is_numerator = models.NullBooleanField(
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
        default=TYPE[0][0]
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name=u'Предмет'
    )
    group = models.ForeignKey(
        GroupSt,
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
    ('delete', 'удалено'),
    ('active', 'активное')
)
class Lesson(BaseModel):
    '''
    Занятие
    '''
    schedule_list = models.ForeignKey(
        ScheduleList,
        verbose_name=u'РАсписание'
    )
    date = models.DateTimeField(
        verbose_name = u'Дата занятия'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=LESSON_STATUS,
        default=LESSON_STATUS[1][0]
    )
    is_end = models.BooleanField(
        verbose_name = u'Завершено',
        default=False
    )

    class Meta:
        verbose_name = u'Занятие'
        verbose_name_plural = u'Занятия'


STATUS_PRESENT = (
    ('present', 'Присутствует'),
    ('missing', 'Отсутствует'),
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
    status_present = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS_PRESENT,
        default=STATUS_PRESENT[0][0]
    )
    note = models.DateTimeField(
        verbose_name = u'Примечание',
        null=True, blank=True
    )

    class Meta:
        verbose_name = u'Присуствие Студента'
        verbose_name_plural = u'Присуствие Студентов'


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
        GroupSt,
        verbose_name = u'Группа'
    )
    schedule = models.ForeignKey(
        ScheduleList,
        verbose_name=u'Расписание'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=TASK_STATUS,
        default=TASK_STATUS[0][0]
    )

    class Meta:
        verbose_name = u'Занятие'
        verbose_name_plural = u'Занятия'


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
        verbose_name = u'Дата сдачи'
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
