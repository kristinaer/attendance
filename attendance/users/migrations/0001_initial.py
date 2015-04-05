# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('f', models.CharField(max_length=254, verbose_name='Фамилия')),
                ('i', models.CharField(max_length=254, verbose_name='Имя')),
                ('o', models.CharField(max_length=254, null=True, verbose_name='Отчество', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания пользователя')),
                ('status', models.CharField(max_length=50, default='active', choices=[('active', 'активный'), ('delete', 'удаленный')], verbose_name='Статус')),
                ('log', models.CharField(max_length=254, unique=True, verbose_name='Логин', db_index=True)),
                ('groups', models.ManyToManyField(related_name='user_set', verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_query_name='user', to='auth.Group')),
                ('user_permissions', models.ManyToManyField(related_name='user_set', verbose_name='user permissions', help_text='Specific permissions for this user.', blank=True, related_query_name='user', to='auth.Permission')),
            ],
            options={
                'verbose_name_plural': 'Пользователи',
                'db_table': 'users',
                'verbose_name': 'Пользователь',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupSt',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(max_length=50, default='active', choices=[('active', 'активная'), ('release', 'выпущенная'), ('delete', 'удаленная')], verbose_name='Статус')),
            ],
            options={
                'verbose_name_plural': 'Группы студентов',
                'verbose_name': 'Группа стедентов',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='GroupStudents',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата зачисления')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Дата отчисления', blank=True)),
                ('groupst', models.ForeignKey(verbose_name='Группа', to='users.GroupSt')),
                ('user', models.ForeignKey(verbose_name='Студент', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Студенты группы',
                'verbose_name': 'Студент группы',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('short_name', models.CharField(max_length=50, verbose_name='Короткое название')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
                ('qualification', models.CharField(max_length=50, default='speciality', choices=[('speciality', 'Специалитет'), ('bachelor', 'Бакалавр'), ('master', 'Магистр'), ('graduate', 'Аспирантура')], verbose_name='Квалификация')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('status', models.CharField(max_length=50, default='active', choices=[('active', 'активная'), ('delete', 'закрытая'), ('delete', 'удаленная')], verbose_name='Статус')),
            ],
            options={
                'verbose_name_plural': 'Специальности',
                'verbose_name': 'Специальность',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.AddField(
            model_name='groupst',
            name='speciality',
            field=models.ForeignKey(verbose_name='Специальность', to='users.Speciality'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='groupst',
            name='starosta',
            field=models.ForeignKey(verbose_name='Староста', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
