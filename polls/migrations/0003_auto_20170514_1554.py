# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20170514_1544'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Corpuses',
        ),
        migrations.AddField(
            model_name='document',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
