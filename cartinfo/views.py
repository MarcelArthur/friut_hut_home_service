from django.shortcuts import render, redirect
from django.http import request, response, HttpResponse
from userinfo.views import login_decorator
from django.db import DatabaseError
from cartinfo.models import CartInfo
import logging
import json
from memberapp.models import Goods
from django.core import serializers
from userinfo.models import UserInfo, Address
# Create your views here.


@login_decorator
def cart_info(request):
    user_id = request.session.get('user_id')
    find_goods = CartInfo.objects.filter(user=user_id)
    cart_foods = {'find_goods': find_goods}
    return render(request, 'cart.html', cart_foods)


@login_decorator
# 添加一个购物车并且跳转 api 实现方法
def add_cart(request):
    '''
    :param request:
    :return:
    :describe: 数据库物品判断和处理
    '''
    new_cart = CartInfo()
    user_id = request.session.get('user_id')
    good_id = request.POST.get('good_id')
    print('商品id', good_id)
    cart_count_good = CartInfo.objects.filter(user=user_id, good=good_id)
    cart_add_count = 0
    # 判断购物车当中是否已添加物品的逻辑
    for i in cart_count_good:
        cart_add_count += 1
    good_count = request.POST.get('gcount')
    good_ = Goods.objects.filter(id=good_id)
    user_ = UserInfo.objects.get(id=user_id)
    new_cart.ccount = good_count
    if len(good_) > 0:
        new_cart.user = user_
        new_cart.good = good_[0]
    else:
        print('添加购物车失败')
        redirect('/cart/')
    try:
        if cart_add_count > 0:
            cart_count_good[0].ccount += int(good_count)
            cart_count_good[0].save()
        else:
            new_cart.save()
    except BaseException as e:
        logging.warning(e)
        raise '数据库插入异常'
        content = {'status': 'Fail', 'text': '添加数据失败', 'cart_count': 0}
        return HttpResponse(json.dumps(content))
    cart_count = CartInfo.objects.filter(user=user_id)
    cart_i = 0
    for i in cart_count:
        cart_i += 1
    cart_count = cart_i
    content = {'status': 'Ok', 'text': '添加数据成功', 'cart_count': cart_count}
    # 1 购物车的动态效果没有实现， 2 购物车的数目统计无法完成
    return HttpResponse(json.dumps(content), content_type='application/json')

@login_decorator
def update_cart(request, id):
    user_id = request.session.get('user_id')
    count = request.GET.get('data')
    Cart = CartInfo.objects.filter(user=user_id, id=id)
    true_count = 0
    for i in Cart:
        true_count += 1
    if true_count > 0:
        Cart[0].ccount = int(count)
        Cart[0].save()
    else:
        raise '非法的请求， 插入失败'
    return HttpResponse(json.dumps({'status': 'OK'}), content_type='application/json')


def create_place_order(request):
    cart_id = request.GET.getlist('cart_id')
    carts = CartInfo.objects.filter(id__in=cart_id)
    abs_ins = ','.join(cart_id)
    addresses = Address.objects.filter(isactive=True)
    if len(cart_id) > 0:
        return render(request, 'place_order.html', {'carts': carts, 'addresses': addresses[0], 'abs_ins': abs_ins})
    else:
        return redirect('/cart/')


def delete_cart(request):
    cart_id = request.POST.get('cart_id')
    user_id = request.session.get('user_id')
    carts = CartInfo.objects.filter(id=cart_id)
    if len(carts) > 0:
        carts.delete()
        status = 'success'
    else:
        status = 'fail'
    carts_list = CartInfo.objects.filter(user=user_id)

    return HttpResponse(json.dumps({'status': status, 'url_d': '/cart/'}), content_type='application/json')




