# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0023_auto_20151201_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='weight',
            field=models.IntegerField(default=1),
        ),
    ]
