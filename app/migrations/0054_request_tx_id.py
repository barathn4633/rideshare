# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-30 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20230430_0318'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='tx_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='transaction ID'),
        ),
    ]