# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_end',
            field=models.BooleanField(verbose_name='Завершено', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='schedulelist',
            name='block_starosta',
            field=models.BooleanField(verbose_name='Заблокировать старосту', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lessonstudents',
            name='status_present',
            field=models.CharField(choices=[('present', 'Присутствует'), ('missing', 'Отсутствует'), ('was_late', 'Опоздал')], verbose_name='Статус', default='present', max_length=50),
            preserve_default=True,
        ),
    ]
