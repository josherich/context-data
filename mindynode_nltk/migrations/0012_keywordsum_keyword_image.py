# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-14 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0011_page_page_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='keywordsum',
            name='keyword_image',
            field=models.CharField(default='', max_length=255, null=True, verbose_name='图片url'),
        ),
    ]
