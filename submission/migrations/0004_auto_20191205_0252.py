# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-05 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_submission_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='use_memory_m_bytes',
            field=models.FloatField(default=0.0),
        ),
    ]