# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150410_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupst',
            name='date_end',
            field=models.DateField(verbose_name='Дата выпуска', null=True),
        ),
    ]
