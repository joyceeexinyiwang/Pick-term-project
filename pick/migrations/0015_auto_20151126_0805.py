# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0014_auto_20151126_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cons',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='post',
            name='pros',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 8, 5, 14, 485039)),
        ),
    ]
