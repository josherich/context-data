# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-03 18:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindynode_nltk', '0016_pagegroup_group_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagegroup',
            name='group_pages',
            field=models.ManyToManyField(to='mindynode_nltk.Page'),
        ),
    ]
