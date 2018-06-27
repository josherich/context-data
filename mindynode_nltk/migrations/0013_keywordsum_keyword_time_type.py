# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-21 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0012_keywordsum_keyword_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordsum',
            name='keyword_time_type',
            field=models.CharField(default='time', max_length=255, null=True, verbose_name='时间类别'),
        ),
    ]
