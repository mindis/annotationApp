# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-11 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_auto_20161011_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotationqueue',
            name='maxAnnoNum',
            field=models.IntegerField(default=0),
        ),
    ]
