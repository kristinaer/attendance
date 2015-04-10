# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20150409_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prepod',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Преподаватели',
                'proxy': True,
                'verbose_name': 'Преподаватель',
            },
            bases=('users.user',),
        ),
    ]
