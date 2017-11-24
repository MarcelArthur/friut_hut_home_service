from django.db import models
from django import forms
# Create your models here.
# class Userinfo(forms.From):... 可以使用内置的表单验证渠道


# 用户信息
class UserInfo(models.Model):
    email = models.CharField('邮箱', max_length=40, db_column='uemail', null=False)
    uname = models.CharField('用户名', max_length=50, db_column='uname', null=False)
    upassword = models.CharField('密码', max_length=200, db_column='upassword', null=False)
    ucellphone = models.CharField('手机', max_length=15, default='086', db_column='ucellphone')
    # uaddress = models.CharField('联系地址', max_length=150, default='无')  一个电商要什么联系地址
    isban = models.BooleanField('禁用', default=False)
    # isactive = models.BooleanField('激活', default = False)
    # ucellphone = models.CharField('手机', default ='086')

    def __str__(self):
        return self.uname

    def get_absolute_url(self):
        return '???'

    class Meta():
        db_table = 'users'


#
class Address(models.Model):
    aname = models.CharField('姓名', max_length=30, db_column='aname', null=False)
    address = models.CharField('详细地址', max_length=150, db_column='address', null=False)
    cellphone = models.CharField('手机号', max_length=15, db_column='cellphone', null=False)
    PostalCode = models.CharField('邮编', max_length=20, db_column='PostalCode', null=False, default='0000000')
    isactive = models.BooleanField('是否为当前地址', default=False)
    user = models.ForeignKey(UserInfo)

    def __str__(self):
        return self.aname

    def get_absolute_url(self):
        return '/user/address/'

    class Meta():
        db_table = 'address'