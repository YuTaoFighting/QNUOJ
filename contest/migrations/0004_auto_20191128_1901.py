# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-28 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20191128_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='rule_type',
            field=models.CharField(choices=[('ACM', 'ACM'), ('OI', 'OI'), ('LanQiaoBei', 'LanQiaoBei')], max_length=12),
        ),
    ]
