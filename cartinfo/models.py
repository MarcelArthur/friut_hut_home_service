from django.db import models
from userinfo.models import UserInfo
from memberapp.models import Goods
# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo, db_column='user_id')
    good = models.ForeignKey(Goods, db_column='good_id')
    ccount = models.IntegerField('数量', db_column='cart_count')

    def __str__(self):
        return self.user.id

    def get_absolute_url(self):
        return '/cart/'

    class Meta():
        db_table = 'cartinfo'