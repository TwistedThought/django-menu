# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-28 18:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuitem_named_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='arg',
            field=models.IntegerField(blank=True, null=True, verbose_name='argument'),
        ),
    ]
