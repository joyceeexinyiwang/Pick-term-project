# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0020_auto_20151127_0837'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Suggester',
        ),
        migrations.RemoveField(
            model_name='post',
            name='picked',
        ),
        migrations.AddField(
            model_name='post',
            name='isResult',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 30, 9, 45, 36, 271846)),
        ),
    ]
