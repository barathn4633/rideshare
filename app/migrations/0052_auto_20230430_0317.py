# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-30 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_auto_20230430_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='bearable',
            field=models.DecimalField(decimal_places=50, max_digits=80, verbose_name='bearable cost'),
        ),
    ]
