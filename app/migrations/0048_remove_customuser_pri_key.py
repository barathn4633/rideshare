# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-30 01:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20230430_0127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='pri_key',
        ),
    ]
