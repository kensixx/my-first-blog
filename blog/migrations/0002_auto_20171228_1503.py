# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-28 07:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='created_name',
            new_name='created_date',
        ),
    ]
