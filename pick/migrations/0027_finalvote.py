# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0026_auto_20151202_0638'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinalVote',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('ratername', models.CharField(default='', max_length=1000)),
                ('option', models.ForeignKey(default='', to='pick.Option')),
            ],
        ),
    ]
