# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 13:46
from __future__ import unicode_literals

import autoslug.fields
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import versionfield


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flow', '0023_update_checksum'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionInRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, max_length=100, populate_from='name', unique_with=('version',))),
                ('version', versionfield.VersionField(default='0.0.0')),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('label', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
                'get_latest_by': 'version',
                'default_permissions': (),
                'permissions': (('view_relation', 'Can view relation'), ('edit_relation', 'Can edit relation'), ('share_relation', 'Can share relation'), ('owner_relation', 'Is owner of the relation')),
            },
        ),
        migrations.CreateModel(
            name='RelationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('ordered', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='relation',
            name='collection',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='flow.Collection'),
        ),
        migrations.AddField(
            model_name='relation',
            name='contributor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='relation',
            name='entities',
            field=models.ManyToManyField(through='flow.PositionInRelation', to='flow.Entity'),
        ),
        migrations.AddField(
            model_name='relation',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='flow.RelationType'),
        ),
        migrations.AddField(
            model_name='positioninrelation',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flow.Entity'),
        ),
        migrations.AddField(
            model_name='positioninrelation',
            name='relation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flow.Relation'),
        ),
        migrations.AlterUniqueTogether(
            name='relation',
            unique_together=set([('slug', 'version')]),
        ),
    ]
