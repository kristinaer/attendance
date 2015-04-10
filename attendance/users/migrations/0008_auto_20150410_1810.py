# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20150410_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speciality',
            name='qualification',
            field=models.CharField(default='speciality', max_length=50, verbose_name='Квалификация', choices=[('speciality', 'Специалитет'), ('bachelor', 'Бакалавриат'), ('master', 'Магистратура'), ('graduate', 'Аспирантура')]),
        ),
    ]
