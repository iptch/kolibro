# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2023-05-12 20:45
from __future__ import unicode_literals

from django.db import migrations, models
import morango.models.fields.uuids


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SyncEntry',
            fields=[
                ('id', morango.models.fields.uuids.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('_morango_dirty_bit', models.BooleanField(default=True, editable=False)),
                ('_morango_source_id', models.CharField(editable=False, max_length=96)),
                ('_morango_partition', models.CharField(editable=False, max_length=128)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        
    ]
