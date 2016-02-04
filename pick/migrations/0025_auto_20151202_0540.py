# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0024_auto_20151202_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='post',
            new_name='option',
        ),
    ]
