# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_auto_20150409_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='short_name',
        ),
        migrations.AlterField(
            model_name='lessonstudents',
            name='note',
            field=models.TextField(null=True, blank=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='taskuser',
            name='note',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
