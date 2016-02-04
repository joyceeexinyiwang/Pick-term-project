# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0016_auto_20151127_0453'),
    ]

    operations = [
        migrations.CreateModel(
            name='Con',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('concontent', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Pro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('procontent', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 5, 6, 8, 65157)),
        ),
        migrations.AddField(
            model_name='pro',
            name='post',
            field=models.ForeignKey(to='pick.Post'),
        ),
        migrations.AddField(
            model_name='con',
            name='post',
            field=models.ForeignKey(to='pick.Post'),
        ),
    ]
