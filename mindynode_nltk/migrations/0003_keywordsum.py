# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-31 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0002_feedkeywords_keyword_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordSum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword_name', models.CharField(default=None, max_length=255, verbose_name='中文名')),
                ('keyword_cal_date', models.DateTimeField(default=None, null=True, verbose_name='计算事件')),
                ('keyword_weight', models.FloatField(default=0, verbose_name='权重')),
                ('keyword_source', models.CharField(default=None, max_length=255, null=True, verbose_name='来源')),
            ],
            options={
                'verbose_name': 'KeywordSum',
                'db_table': 'feed_keywords_sum',
                'verbose_name_plural': 'KeywordSum',
            },
        ),
    ]
