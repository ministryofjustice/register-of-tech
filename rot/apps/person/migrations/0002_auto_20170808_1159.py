# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-08 11:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['last_name'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
