# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-05 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yourtips', '0002_create_index_tip_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yourtipsentry',
            name='converted_article_page',
            field=models.ForeignKey(blank=True, help_text='Your tip article page to which the entry was converted to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tip_entries', to='yourtips.YourTipsArticlePage'),
        ),
    ]
