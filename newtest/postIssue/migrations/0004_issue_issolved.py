# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-29 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postIssue', '0003_auto_20160525_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='isSolved',
            field=models.BooleanField(default=False),
        ),
    ]
