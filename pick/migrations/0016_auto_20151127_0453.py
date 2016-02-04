# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0015_auto_20151126_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggester',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='cons',
        ),
        migrations.RemoveField(
            model_name='post',
            name='pros',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 4, 53, 11, 437189)),
        ),
    ]
