# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-10 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0038_auto_20151210_2027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstatts',
            old_name='solvedProblems',
            new_name='solved_problems',
        ),
        migrations.RenameField(
            model_name='userstatts',
            old_name='triedProblems',
            new_name='tried_problems',
        ),
    ]
