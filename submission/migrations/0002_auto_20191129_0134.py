# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-29 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='result',
            field=models.IntegerField(db_index=True, default=10),
        ),
    ]
