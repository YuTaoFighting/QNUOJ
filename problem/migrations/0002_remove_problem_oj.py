# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-27 23:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='oj',
        ),
    ]