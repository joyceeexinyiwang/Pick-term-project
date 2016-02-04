# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0018_auto_20151127_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='votedBy',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 5, 58, 0, 988555)),
        ),
    ]
