# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0022_auto_20151130_2219'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(default='', max_length=1000)),
                ('totalRate', models.IntegerField(default=0)),
                ('numberOfRater', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(default='', max_length=1000)),
                ('optionContent', models.CharField(max_length=1000)),
                ('isResult', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Goal',
        ),
        migrations.RenameField(
            model_name='rate',
            old_name='votes',
            new_name='number',
        ),
        migrations.RemoveField(
            model_name='con',
            name='post',
        ),
        migrations.RemoveField(
            model_name='pro',
            name='post',
        ),
        migrations.AlterField(
            model_name='rate',
            name='post',
            field=models.ForeignKey(default='', to='pick.Option'),
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='criterion',
            name='option',
            field=models.ForeignKey(default='', to='pick.Option'),
        ),
        migrations.AddField(
            model_name='con',
            name='option',
            field=models.ForeignKey(default='', to='pick.Option'),
        ),
        migrations.AddField(
            model_name='pro',
            name='option',
            field=models.ForeignKey(default='', to='pick.Option'),
        ),
        migrations.AddField(
            model_name='rate',
            name='criterion',
            field=models.ForeignKey(default='', to='pick.Criterion'),
        ),
    ]
