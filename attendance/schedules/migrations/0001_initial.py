# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('date', models.DateTimeField(verbose_name='Дата занятия')),
                ('status', models.CharField(verbose_name='Статус', max_length=50, default='standart', choices=[('delete', 'отменен'), ('replace', 'перенесен'), ('standart', 'обычно')])),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='LessonStudents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status_present', models.BooleanField(verbose_name='Статус', max_length=50, default='present', choices=[('present', 'Присутствует'), ('missing', 'Отсутствует'), ('was_late', 'Опоздал')])),
                ('note', models.DateTimeField(blank=True, verbose_name='Примечание', null=True)),
                ('lesson', models.ForeignKey(to='schedules.Lesson', verbose_name='Занятие')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Присуствие Студента',
                'verbose_name_plural': 'Присуствие Студентов',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('year', models.CharField(verbose_name='Год', max_length=254)),
                ('start_date', models.DateTimeField(verbose_name='Дата начала')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('osen_vesna', models.CharField(verbose_name='Осень/весна', max_length=50, default='osen', choices=[('osen', 'Осень'), ('vesna', 'Весна')])),
                ('is_numerator', models.BooleanField(verbose_name='Числитель', default=True)),
                ('status', models.CharField(verbose_name='Статус', max_length=50, default='active', choices=[('active', 'активный'), ('delete', 'удаленный')])),
            ],
            options={
                'verbose_name': 'Учебный год',
                'verbose_name_plural': 'Учебные года',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='ScheduleList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('weekday', models.IntegerField(verbose_name='День недели')),
                ('is_numerator', models.NullBooleanField(verbose_name='Числитель', default=True)),
                ('number_pairs', models.IntegerField(verbose_name='Номер пары')),
                ('type', models.CharField(verbose_name='Тип', max_length=50, default='lecture', choices=[('lecture', 'Лекция'), ('practice', 'Практика')])),
                ('group', models.ForeignKey(to='users.GroupSt', verbose_name='Группа')),
                ('schedule', models.ForeignKey(to='schedules.Schedule', verbose_name='Учебный год')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписание',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='Название', max_length=254)),
                ('short_name', models.CharField(verbose_name='Короткое название', max_length=50)),
                ('description', models.CharField(verbose_name='Описание', max_length=250)),
                ('created_at', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('status', models.CharField(verbose_name='Статус', max_length=50, default='active', choices=[('active', 'активный'), ('delete', 'удаленный')])),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Название', max_length=254)),
                ('created_at', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('description', models.CharField(verbose_name='Описание', max_length=250)),
                ('delivery_date', models.DateTimeField(blank=True, verbose_name='Дата сдачи', null=True)),
                ('status', models.CharField(verbose_name='Статус', max_length=50, default='active', choices=[('active', 'активное'), ('delete', 'удаленное')])),
                ('group', models.ForeignKey(to='users.GroupSt', verbose_name='Группа')),
                ('schedule', models.ForeignKey(to='schedules.ScheduleList', verbose_name='Расписание')),
                ('subject', models.ForeignKey(to='schedules.Subject', verbose_name='Предмет')),
                ('teacher', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Преподаватель')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.CreateModel(
            name='TaskUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)),
                ('date', models.DateTimeField(verbose_name='Дата')),
                ('note', models.CharField(verbose_name='Описание', max_length=250)),
                ('is_pass', models.BooleanField(verbose_name='Сдано', default=False)),
                ('task', models.ForeignKey(to='schedules.Task', verbose_name='Задание')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': 'Сдача задания',
                'verbose_name_plural': 'Сдача заданий',
            },
            bases=(models.Model, core.models.AttendanceMixins),
        ),
        migrations.AddField(
            model_name='schedulelist',
            name='subject',
            field=models.ForeignKey(to='schedules.Subject', verbose_name='Предмет'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedulelist',
            name='teacher',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Преподаватель'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lesson',
            name='schedule_list',
            field=models.ForeignKey(to='schedules.ScheduleList', verbose_name='РАсписание'),
            preserve_default=True,
        ),
    ]
