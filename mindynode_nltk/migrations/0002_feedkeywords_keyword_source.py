# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-30 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedkeywords',
            name='keyword_source',
            field=models.CharField(default=None, max_length=255, null=True, verbose_name='来源'),
        ),
    ]
