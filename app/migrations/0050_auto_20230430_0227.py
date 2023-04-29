# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2023-04-30 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_customuser_private_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='bearable',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='bearable cost'),
        ),
    ]
