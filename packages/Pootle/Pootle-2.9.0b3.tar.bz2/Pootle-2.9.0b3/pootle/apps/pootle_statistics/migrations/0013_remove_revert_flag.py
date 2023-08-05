# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-25 14:15
from __future__ import unicode_literals

from django.db import migrations

# this was the value of SubmissionTypes.REVERT
REVERT_FLAG = 2

def remove_revert_flag(apps, schema_editor):
    subs = apps.get_model("pootle_statistics.Submission").objects.all()
    subs.filter(type=REVERT_FLAG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_statistics', '0012_remove_create_subs'),
    ]

    operations = [
        migrations.RunPython(remove_revert_flag),
    ]
