# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-14 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0010_keywordsum_keyword_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='page_image',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='图片url'),
        ),
    ]