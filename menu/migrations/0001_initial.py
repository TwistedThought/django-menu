# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-19 08:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='caption')),
                ('url', models.CharField(blank=True, max_length=200, verbose_name='URL')),
                ('level', models.IntegerField(default=0, editable=False, verbose_name='level')),
                ('rank', models.IntegerField(default=0, editable=False, verbose_name='rank')),
                ('menu', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contained_items', to='menu.Menu', verbose_name='menu')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.MenuItem', verbose_name='parent')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='root_item',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='is_root_item_of', to='menu.MenuItem', verbose_name='root item'),
        ),
    ]
