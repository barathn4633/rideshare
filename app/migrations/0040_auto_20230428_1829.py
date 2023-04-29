# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-28 18:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20230428_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='k',
        ),
        migrations.AddField(
            model_name='customuser',
            name='wallet_address',
            field=models.CharField(default='', help_text='Required. Ethereum address in hex format (without "0x" prefix).', max_length=42, validators=[django.core.validators.RegexValidator(re.compile('^[a-fA-F0-9]{40}$', 32), 'Enter a valid wallet address.', 'invalid')], verbose_name='Wallet address'),
            preserve_default=False,
        ),
    ]
