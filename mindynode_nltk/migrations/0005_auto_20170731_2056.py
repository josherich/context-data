# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-31 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0004_stopword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stopword',
            name='stopword_category',
            field=models.CharField(default='general', max_length=255, null=True, verbose_name='类别名'),
        ),
    ]
