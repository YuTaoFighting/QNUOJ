# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-05 02:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20191205_0252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='use_memory_m_bytes',
            new_name='use_memory_bytes',
        ),
    ]
