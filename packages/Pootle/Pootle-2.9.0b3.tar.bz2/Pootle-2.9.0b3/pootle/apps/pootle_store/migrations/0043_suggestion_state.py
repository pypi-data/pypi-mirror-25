# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 05:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_store', '0042_add_default_suggestion_states'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suggestions', to='pootle_store.SuggestionState'),
        ),
    ]
