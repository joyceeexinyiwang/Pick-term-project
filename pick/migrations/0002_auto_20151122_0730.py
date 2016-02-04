# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pick', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='suggester',
        ),
        migrations.DeleteModel(
            name='Suggester',
        ),
    ]
