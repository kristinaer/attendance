# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20150410_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
