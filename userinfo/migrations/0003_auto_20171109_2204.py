# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-09 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0002_userinfo_ucellphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='PostalCode',
            field=models.CharField(db_column='PostalCode', default='0000000', max_length=20, verbose_name='邮编'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(db_column='address', max_length=150, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ucellphone',
            field=models.CharField(db_column='ucellphone', default='086', max_length=15, verbose_name='手机'),
        ),
    ]
