# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_auto_20150405_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedulelist',
            name='block_starosta',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='status',
            field=models.CharField(default='active', max_length=50, choices=[('delete', 'удалено'), ('active', 'активное')], verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='taskuser',
            name='date',
            field=models.DateTimeField(verbose_name='Дата сдачи'),
        ),
    ]
