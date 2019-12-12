# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-08 22:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_userprofile_ac_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contest_id', models.IntegerField()),
                ('contest_title', models.TextField()),
                ('contest_begin_time', models.DateTimeField()),
                ('rating', models.FloatField(default=1500.0)),
                ('change', models.FloatField(default=0.0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.User')),
            ],
            options={
                'db_table': 'rating_change',
            },
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together=set([('user', 'contest_id')]),
        ),
    ]