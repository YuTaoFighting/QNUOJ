# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-20 20:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_name', models.CharField(max_length=64, unique=True)),
            ],
            options={
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='role',
            name='users',
            field=models.ManyToManyField(to='account.User'),
        ),
    ]
