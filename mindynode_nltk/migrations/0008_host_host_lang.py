# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-02 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0007_auto_20170801_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_lang',
            field=models.CharField(default='zh', max_length=255, null=True, verbose_name='语言'),
        ),
    ]
