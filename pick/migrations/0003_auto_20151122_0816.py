# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0002_auto_20151122_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picked',
            field=models.BooleanField(default=True),
        ),
    ]
