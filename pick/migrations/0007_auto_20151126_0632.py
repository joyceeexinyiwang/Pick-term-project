# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0006_auto_20151126_0552'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='goal_content',
            new_name='gcontent',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 6, 32, 31, 659131)),
        ),
    ]
