# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-17 17:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0046_auto_20151217_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='grader_message',
            field=models.CharField(default='In Queue', max_length=32),
        ),
    ]