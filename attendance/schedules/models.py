# -*- coding: utf-8 -*-
'''
Расписание
'''
from django.db import models

from users.models import User, GroupSt, Speciality
from core.models import BaseModel


STATUS = (
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
        verbose_name = u'Короткое_название',
        max_length = 25,
    )
    description = models.TextField(
        verbose_name = u'Описание'
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )
    class Meta:
        verbose_name = u'Предмет'
        verbose_name_plural = u'Предметы'

class SpecialitySubject(BaseModel):
    '''
    Специальности предметы
    '''
    subject = models.ForeignKey(
        Subject,
        verbose_name = u'Предмет',
    )
    speciality = models.ForeignKey(
        Speciality,
        verbose_name = u'Специальность',
    )
    semestr = models.IntegerField(
        verbose_name = u'Семестр',
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )

    class Meta:
        verbose_name = u'Специальность предметы'
        verbose_name_plural = u'Специальности предметы'

SCHOOLYEAR_STATUS = (
    ('active', 'активный'),
    ('delete', 'удаленный'),
    ('new', 'новый'),
    ('archiv', 'архивный')
)
OSEN_VESNA_STATUS = (
    ('osen', 'Осень'),
    ('vesna', 'Весна')
)
class Schoolyear(BaseModel):
    '''
    Учебный год
    '''
    year = models.CharField(
        verbose_name = u'Год',
        max_length = 4,
    )
    osen_vesna = models.CharField(
        verbose_name = u'Осень/весна',
        max_length = 50,
        choices=OSEN_VESNA_STATUS,
        default=OSEN_VESNA_STATUS[0][0]
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=SCHOOLYEAR_STATUS,
        default=SCHOOLYEAR_STATUS[0][0]
    )
    def __unicode__(self):
        return '%s %s' % (self.year, self.osen_vesna)

    class Meta:
        verbose_name = u'Учебный год'
        verbose_name_plural = u'Учебные года'


class Schedule(BaseModel):
    '''
    Расписание
    '''
    semestr = models.IntegerField(
        verbose_name = u'Семестр',
    )
    group = models.ForeignKey(
        GroupSt,
        verbose_name = u'Группа',
    )
    schoolyear = models.ForeignKey(
        Schoolyear,
        verbose_name = u'Учебный год',
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )

    def __unicode__(self):
        return '%s %s %s' % (self.schoolyear.year, self.schoolyear.osen_vesna, self.group.name)

    class Meta:
        verbose_name = u'Расписание'
        verbose_name_plural = u'Расписание'


class ScheduleList(BaseModel):
    '''
    Лист расписания
    '''
    subject = models.ForeignKey(
        Subject,
        verbose_name = u'Предмет'
    )
    prepod = models.ForeignKey(
        User,
        verbose_name = u'Преподаватель',
        null=True, blank=True
    )
    schedule = models.ForeignKey(
        Schedule,
        verbose_name = u'Расписание'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )

    class Meta:
        verbose_name = u'Лист расписания'
        verbose_name_plural = u'Лист расписания'


TYPE = (
    ('lecture', 'Лекция'),
    ('practice', 'Практика')
)
class Lesson(BaseModel):
    '''
    Занятие
    '''
    schedule_list = models.ForeignKey(
        ScheduleList,
        verbose_name=u'Расписание'
    )
    date = models.DateTimeField(
        verbose_name = u'Дата занятия'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )
    topic = models.CharField(
        verbose_name=u'Тема',
        max_length=255
    )
    type = models.CharField(
        verbose_name = u'Тип',
        max_length = 50,
        choices=TYPE,
        default=TYPE[0][0]
    )
    class Meta:
        verbose_name = u'Занятие'
        verbose_name_plural = u'Занятия'


STATUS_PRESENT = (
    ('present', 'Присутствует'),
    ('missing', 'Отсутствует')
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

    class Meta:
        verbose_name = u'Присуствие Студента'
        verbose_name_plural = u'Присуствие Студентов'
