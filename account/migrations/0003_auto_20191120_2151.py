# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-20 21:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_permission'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_problems', models.TextField(blank=True, default='')),
                ('realname', models.TextField(null=True)),
                ('avatar', models.TextField(null=True)),
                ('blog', models.URLField(null=True)),
                ('github', models.TextField(null=True)),
                ('school', models.TextField(null=True)),
                ('major', models.TextField(null=True)),
                ('rating', models.FloatField(default=1500.0)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.User'),
        ),
    ]
