# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150410_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupst',
            name='date_end',
            field=models.DateTimeField(null=True, verbose_name='Дата выпуска'),
        ),
        migrations.AlterField(
            model_name='groupst',
            name='starosta',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, verbose_name='Староста', blank=True),
        ),
        migrations.AlterField(
            model_name='groupst',
            name='status',
            field=models.CharField(max_length=50, choices=[('active', 'активная'), ('delete', 'удаленная')], verbose_name='Статус', default='active'),
        ),
    ]
