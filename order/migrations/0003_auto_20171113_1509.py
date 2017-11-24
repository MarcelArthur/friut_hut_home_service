# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 07:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_orderinfo_isdelete_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='count',
            field=models.IntegerField(db_column='order_count', verbose_name='订单物品数量'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(db_column='order_id', on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='create_order',
            field=models.DateTimeField(auto_now_add=True, verbose_name='订单生成时间'),
        ),
    ]
