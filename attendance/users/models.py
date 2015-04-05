# -*- coding: utf-8 -*-
'''
Пользователи, роли, права
'''
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import login, authenticate

from users.managers import UserManager
from core.models import BaseModel


USERS_STATUS = (
    ('active', 'активный'),
    ('delete', 'удаленный')
)
class User(AbstractBaseUser, PermissionsMixin):
    '''
    Пользователь
    '''
    f = models.CharField(
        verbose_name = u'Фамилия',
        max_length = 254,
    )
    i = models.CharField(
        verbose_name = u'Имя',
        max_length = 254,
    )
    o = models.CharField(
        verbose_name = u'Отчество',
        max_length = 254,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания пользователя',
        auto_now_add = True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=USERS_STATUS,
        default='active'
    )
    log = models.CharField(
        verbose_name = u'Логин',
        max_length = 254,
        unique = True,
        db_index = True,
    )
    objects = UserManager()

    def get_full_name(self):
        return '%s %s %s' % (self.f, self.i, self.o)

    def get_short_name(self):
        if self.o:
            return '%s %s. %s.' % (self.f, self.i[0], self.o[0])
        else:
            return '%s %s.' % (self.f, self.i[0])

    def force_login(self, request):
        self.is_internal_auth_mode = True
        authenticate(user=self)
        login(request, self)

    USERNAME_FIELD = 'log'

    def __unicode__(self):
        return self.get_short_name()

    class Meta:
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'


QUALIFICATIONS = (
    ('speciality', 'Специалитет'),
    ('bachelor', 'Бакалавр'),
    ('master', 'Магистр'),
    ('graduate', 'Аспирантура'),
)
SPECIALITY_STATUS = (
    ('active', 'активная'),
    ('delete', 'закрытая'),
    ('delete', 'удаленная')
)
class Speciality(BaseModel):
    '''
    Специальности
    '''
    name = models.CharField(
        verbose_name=u'Название',
        max_length=255,
    )
    short_name = models.CharField(
        verbose_name=u'Короткое название',
        max_length=50,
    )
    description = models.CharField(
        verbose_name=u'Описание',
        max_length=255,
    )
    qualification = models.CharField(
        verbose_name = u'Квалификация',
        max_length = 50,
        choices=QUALIFICATIONS,
        default='speciality'
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=SPECIALITY_STATUS,
        default='active'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'


GROUP_STATUS = (
    ('active', 'активная'),
    ('delete', 'выпущенная')
    ('delete', 'удаленная')
)
class GroupS(BaseModel):
    '''
    Группа студентов
    '''
    name = models.CharField(
        verbose_name=u'Название',
        max_length=255,
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        auto_now_add = True
    )
    speciality = models.ForeignKey(
        Speciality,
        verbose_name = u'Специальность',
    )
    starosta = models.ForeignKey(
        User,
        verbose_name = u'Староста',
        null=True, blank=True,
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=GROUP_STATUS,
        default='active'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Группа стедентов'
        verbose_name_plural = u'Группы студентов'


class GroupStudents(BaseModel):
    '''
    Студенты группы
    '''
    user = models.ForeignKey(
        User,
        verbose_name = u'Студент',
    )
    group = models.ForeignKey(
        GroupS,
        verbose_name = u'Группа',
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата зачисления',
        auto_now_add = True
    )
    deleted_at = models.DateTimeField(
        verbose_name = u'Дата отчисления',
        null=True, blank=True
    )

    class Meta:
        verbose_name = u'Студент группы'
        verbose_name_plural = u'Студенты группы'
