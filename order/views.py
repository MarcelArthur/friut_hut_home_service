from django.shortcuts import render, redirect
from django.http import request, HttpResponse
from django.db import DatabaseError
from django.db.transaction import atomic
from flask import json

from userinfo.models import Address, UserInfo
from userinfo.views import login_decorator
from .models import *
from cartinfo.models import CartInfo
# Create your views here.
# 可以修改为返回本地的局部变量locals()
# 设置事务 要么被提交要么被回滚 设置回滚状态位置点 如果出现异常则回滚
@atomic
@login_decorator
def create_order(request):
    # atomic(savepoint=)
    user_id = request.session.get('user_id')
    address = Address.objects.filter(isactive=True)[0]
    total = request.POST.get('total')
    user = UserInfo.objects.get(id=user_id)
    abs_ins = request.POST.get('abs_ins')
    abs_ins_list = abs_ins.split(',')
    cart_list = CartInfo.objects.filter(id__in=abs_ins_list)
    with atomic():
        if len(cart_list) > 0:
            new_order = OrderInfo()
            new_order.user = user
            new_order.address_site = address
            new_order.total = total
            new_order.save()
            for i in cart_list:
                new_order_detail = OrderDetail()
                new_order_detail.order = new_order
                new_order_detail.good_id = i.good.id
                new_order_detail.count = i.ccount
                new_order_detail.price = i.good.price
                new_order_detail.save()
            print('生成订单和订单明细完成')
            cart_list.delete()

    order_list = OrderInfo.objects.filter(user=user_id)
    if len(order_list) > 0:
        content = {'status': 'Ok'}
    else:
        content = {'status': 'Fail'}
    return HttpResponse(json.dumps(content), content_type='application/json')

    # 设置回滚位置点
    # 订单被保存
    # 订单详情被保存
    # 事务提交
    # else 事务未提交 则回滚
    # 提交 完成则执行 删除购物车 里的相关物品
    # 跳转到订单页面 系统完成


# 重用一下分页逻辑然后展示一下就行了
@login_decorator
def order_all(request):
    user_id = request.session.get('user_id')
    order_list = OrderInfo.objects.filter(user=user_id)

    return render(request, 'user_center_order.html', {'order_list' : order_list})