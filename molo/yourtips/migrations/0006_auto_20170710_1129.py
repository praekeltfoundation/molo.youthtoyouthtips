# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-10 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yourtips', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yourtip',
            name='homepage_action_copy',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Homepage Banner Copy'),
        ),
    ]
