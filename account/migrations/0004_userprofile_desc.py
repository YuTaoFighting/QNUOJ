# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-27 20:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20191125_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='desc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
