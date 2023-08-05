# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-02 19:02
from __future__ import unicode_literals

from django.db import migrations


def add_system_user(apps, schema_editor):
    User = apps.get_model("accounts.User")
    sysuser = User.objects.filter(username="system")
    if not sysuser.exists():
        User.objects.create(
            username="system",
            full_name="Pootle",
            is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_update_system_username'),
    ]

    operations = [
        migrations.RunPython(add_system_user),
    ]
