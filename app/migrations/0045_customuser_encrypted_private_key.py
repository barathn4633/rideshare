# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-30 01:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_request_payment_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='encrypted_private_key',
            field=models.TextField(blank=True),
        ),
    ]
