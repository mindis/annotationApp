# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0003_document_preprocessed'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbc_class_count',
            name='total_word_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
