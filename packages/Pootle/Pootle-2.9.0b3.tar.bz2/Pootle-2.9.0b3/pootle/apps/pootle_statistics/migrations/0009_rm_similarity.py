# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 17:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_statistics', '0008_set_submission_revisions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scorelog',
            name='similarity',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='mt_similarity',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='similarity',
        ),
    ]
