# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20150410_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='status',
            field=models.CharField(choices=[('active', 'активная'), ('delete', 'удаленная')], verbose_name='Статус', max_length=50, default='active'),
        ),
    ]
