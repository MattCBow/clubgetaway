# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(unique=True)),
                ('assignments', models.ManyToManyField(to='scheduler.Assigment')),
            ],
        ),
    ]
