# -*- coding: utf-8 -*-
'''
Пользователи, роли, права
'''
import datetime
import pytils

from hashlib import sha1
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import BaseUserManager as UserManager
from django.contrib.auth.models import Group
from django_hosts import reverse_full
from core.models import BaseModel


STATUS = (
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
    log = models.CharField(
        verbose_name = u'Логин',
        max_length = 254,
        unique = True,
        db_index = True,
    )
    # Фикс
    is_active = models.BooleanField(
        verbose_name = u'Активный',
        default=False
    )
    is_staff = models.BooleanField(
        u'Персонал',
        default=False,
        help_text= u'Может ли пользователь авторизовываться в админке'
    )

    groupsts = models.ManyToManyField(
        'GroupSt',
        verbose_name=u'Группа',
        through = 'GroupStudents'
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.password = User.objects.make_random_password()
        super(User, self).save( *args, **kwargs)

    def get_full_name(self):
        return '%s %s %s' % (self.f, self.i, self.o)

    def get_short_name(self):
        if self.o:
            return '%s %s. %s.' % (self.f, self.i[0], self.o[0])
        else:
            return '%s %s.' % (self.f, self.i[0])

    def check_password(self, raw_password):
        '''
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        '''
        return self.password == raw_password

    def set_password(self, raw_password):
        self.password = raw_password

    def force_login(self, request):
        self.is_internal_auth_mode = True
        authenticate(user=self)
        login(request, self)

    objects = UserManager()

    USERNAME_FIELD = 'log'

    def __unicode__(self):
        return self.get_short_name()

    class Meta:
        db_table = 'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'


class Prepod(User):
    class Meta:
        proxy = True
        verbose_name = u'Преподаватель'
        verbose_name_plural = u'Преподаватели'

    def save(self, *args, **kwargs):
        if not self.id:
            self.is_staff = True
            log = pytils.translit.translify(self.f.lower())
            users = User.objects.filter(log__startswith=log)
            if users:
                log = '%s%s' % (log, users.__len__())
            self.log = log
        super(Prepod, self).save(*args, **kwargs)
        groups = Group.objects.filter(name=u'Преподаватели').all()
        self.groups.add(groups[0])


class Student(User):
    class Meta:
        proxy = True
        verbose_name = u'Студент'
        verbose_name_plural = u'Студенты'


QUALIFICATIONS = (
    ('speciality', 'Специалитет'),
    ('bachelor', 'Бакалавриат'),
    ('master', 'Магистратура'),
    ('graduate', 'Аспирантура'),
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
        verbose_name=u'Короткое_название',
        max_length=25,
    )
    description = models.TextField(
        verbose_name=u'Описание'
    )
    qualification = models.CharField(
        verbose_name = u'Квалификация',
        max_length = 50,
        choices=QUALIFICATIONS,
        default=QUALIFICATIONS[0][0]
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
    #subjects = models.ManyToManyField(
    #    'Subject',
    #    verbose_name=u'Предметы',
    #    through = 'SpecialitySubject'
    #)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'Специальность'
        verbose_name_plural = u'Специальности'


class GroupSt(BaseModel):
    '''
    Группа студентов
    '''
    name = models.CharField(
        verbose_name=u'Название',
        max_length=255,
    )
    created_at = models.DateTimeField(
        verbose_name = u'Дата создания',
        default=datetime.datetime.now
    )
    speciality = models.ForeignKey(
        Speciality,
        verbose_name = u'Специальность',
    )
    starosta = models.ForeignKey(
        User,
        verbose_name = u'Староста',
        null=True, blank=True,
        related_name='%(class)s_starosta'
    )
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )
    users = models.ManyToManyField(
        'User',
        verbose_name=u'Студенты',
        through = 'GroupStudents'
    )

    def link_edit(self):
        return reverse_full(
            'base',
            'users_frontend:group_edit',
            view_kwargs={'pk': self.pk}
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
    groupst = models.ForeignKey(
        GroupSt,
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
    status = models.CharField(
        verbose_name = u'Статус',
        max_length = 50,
        choices=STATUS,
        default=STATUS[0][0]
    )

    class Meta:
        verbose_name = u'Студент группы'
        verbose_name_plural = u'Студенты группы'
