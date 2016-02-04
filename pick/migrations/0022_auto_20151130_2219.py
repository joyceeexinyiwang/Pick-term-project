# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0021_auto_20151130_0945'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ratername', models.CharField(default='', max_length=1000)),
                ('votes', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='votes',
            new_name='totalVotes',
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 30, 22, 19, 31, 226118)),
        ),
        migrations.AddField(
            model_name='rate',
            name='post',
            field=models.ForeignKey(to='pick.Post'),
        ),
    ]
