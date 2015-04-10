# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_prepod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'Студент',
                'verbose_name_plural': 'Студенты',
            },
            bases=('users.user',),
        ),
        migrations.RemoveField(
            model_name='speciality',
            name='short_name',
        ),
    ]
