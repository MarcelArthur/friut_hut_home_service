from django.db import models
from userinfo.models import *
from memberapp.models import *


# Create your models here.
class OrderInfo(models.Model):
    user = models.ForeignKey(UserInfo, db_column='user_id')
    address_site = models.ForeignKey(Address, db_column='address_id')
    total = models.DecimalField(max_digits=8, decimal_places=2)
    create_order = models.DateTimeField('订单生成时间', auto_now_add=True)
    isdelete_order = models.BooleanField('是否删除订单', default=False)

    def __str__(self):
        return self.total

    class Meta():
        db_table = 'Order_Info'


# class OrderLine(models.Model):

class OrderDetail(models.Model):
    good =models.ForeignKey(Goods, db_column='good_id')
    order = models.ForeignKey(OrderInfo, db_column='order_id')
    count = models.IntegerField('订单物品数量', db_column='order_count')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta():
        db_table = 'Order_Detail'