# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-27 05:37
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0012_require_checksum'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='requirements',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
