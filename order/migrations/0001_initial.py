# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 13:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userinfo', '0004_address_isactive'),
        ('memberapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(db_column='order_count_id', verbose_name='订单物品数量')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('good', models.ForeignKey(db_column='good_id', on_delete=django.db.models.deletion.CASCADE, to='memberapp.Goods')),
            ],
            options={
                'db_table': 'Order_Detail',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('create_order', models.DateTimeField(auto_now_add=True)),
                ('address_site', models.ForeignKey(db_column='address_id', on_delete=django.db.models.deletion.CASCADE, to='userinfo.Address')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='userinfo.UserInfo')),
            ],
            options={
                'db_table': 'Order_Info',
            },
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(db_column='detail_id', on_delete=django.db.models.deletion.CASCADE, to='order.OrderInfo'),
        ),
    ]