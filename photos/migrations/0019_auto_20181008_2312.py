# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-08 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0018_auto_20181008_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(max_length=1000),
        ),
    ]
