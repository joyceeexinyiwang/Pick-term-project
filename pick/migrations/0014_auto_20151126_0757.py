# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0013_auto_20151126_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='post',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 7, 57, 40, 966971)),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]
