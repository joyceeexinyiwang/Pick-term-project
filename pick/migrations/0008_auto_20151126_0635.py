# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0007_auto_20151126_0632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='gcontent',
            new_name='goal_content',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 6, 35, 10, 639036)),
        ),
    ]
