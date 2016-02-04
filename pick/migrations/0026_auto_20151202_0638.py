# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0025_auto_20151202_0540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='criterion',
            name='numberOfRater',
        ),
        migrations.RemoveField(
            model_name='criterion',
            name='totalRate',
        ),
    ]
