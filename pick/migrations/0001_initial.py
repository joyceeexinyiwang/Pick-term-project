# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('content', models.CharField(max_length=1000)),
                ('votes', models.IntegerField(default=0)),
                ('picked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Suggester',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('value', models.IntegerField(default=0)),
                ('post', models.ForeignKey(to='pick.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='suggester',
            field=models.ForeignKey(to='pick.Suggester'),
        ),
    ]
