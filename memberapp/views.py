from django.shortcuts import render, get_object_or_404, redirect
from django.http import request, response, HttpRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError, DatabaseError
import logging
import random
import math

from cartinfo.models import CartInfo
from .models import *
# Create your views here.
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.cache import get_cache_key
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', 20 * 60)  # 设置一个缓存键失效时间 在缓存到期时自动失效


# 视图缓存过期
def expire_page(path, curreq,args=None, key_prefix=None):
    if args is None:
        path = reverse(path)
    else:
        path = reverse(path, args=args)

    http_host = curreq.META.get("HTTP_HOST", "")
    if len(http_host.split(":")) == 1:
        server_name, server_port = http_host, "80"        # 如果判断没有端口则可能为80端口访问或者443端口HTTPS访问
    else:
        server_name, server_port = http_host.split(":")

    request = HttpRequest()
    request.META = {'SERVER_NAME': server_name, 'SERVER_PORT': server_port}
    request.META.update(dict((header, value) for (header, value) in
                             curreq.META.items() if header.startswith('HTTP_')))
    request.path = path
    key = get_cache_key(request, key_prefix=key_prefix)
    if cache.has_key(key):
        cache.set(key, None, 0)

# 共用分页逻辑
# 自己实现的分页逻辑(然而并没有什么卵用)
# 匹配当前页 index == (x for x in 总页数)
# def pange_index(goods, index):
#     index = int(index)
#     if int(index) <= 0:
#         index = 1
#     try:
#         goods_counts = goods.objects.count()
#         counts_index = math.ceil(goods_counts / 10)
#         if index >= counts_index:
#             index = counts_index
#             index_page = goods.objects.all()[(index - 1) * 10:]
#         else:
#             index_page = goods.objects.all()[(index - 1) * 10 : index * 10]
#     except DatabaseError as e:
#         logging.warning(e)
#     return index_page, counts_index


# 抽象出的通用的分页逻辑 django自带支持的
def page_index(goods, index, Type):
    if not Type:
        contact_list = goods.objects.all()
    else:
        goods_type = get_object_or_404(GoodsType,title=Type)
        contact_list = goods_type.goods_set.all()
    # 目前来看的效果
    paginator = Paginator(contact_list, 10, 2)
    p_totalpage = paginator.page_range
    try:
        good_contact = paginator.page(index)
    except PageNotAnInteger:
        good_contact = paginator.page(1)
    except EmptyPage:
        good_contact = paginator.page(paginator.num_pages)
    return good_contact

# 首页的展示逻辑 待优化(ajax)
@cache_page(15 * 60)
def index(request):
    cart_count = 0
    try:
        good_fruit_type = get_object_or_404(GoodsType, title='新鲜水果')
        fruit_goods = random.sample(list(good_fruit_type.goods_set.all()), 4)
        good_fruit_meet = get_object_or_404(GoodsType, title='精品肉类')
        meet_goods = random.sample(list(good_fruit_meet.goods_set.all()), 4)
        good_fruit_water = get_object_or_404(GoodsType, title='海鲜水产')
        water_goods = random.sample(list(good_fruit_water.goods_set.all()), 4)
        vagetables_good_type = get_object_or_404(GoodsType, title='新鲜蔬菜')
        vegetables_good = random.sample(list(vagetables_good_type.goods_set.all()), 4)
        quick_snacks_good = get_object_or_404(GoodsType, title='速冻食品')
        quick_food = random.sample(list(quick_snacks_good.goods_set.all()), 4)
        egg_goods_type = get_object_or_404(GoodsType, title='禽类蛋品')
        eggs_foods = random.sample(list(egg_goods_type.goods_set.all()), 4)
        if request.session.get('user_id', None):
            user_id = request.session.get('user_id', None)
            cart_ = CartInfo.objects.filter(user=user_id)
            cart_count = len(cart_)
    except DatabaseError as e:
        logging.warning(e)
    return render(request, 'index.html', {'good_list': locals(), 'cart_count':cart_count})


# 商品列表页的展示逻辑(代码的复用性)
def prolist_list(request, Type=None):
    idv = request.GET.get('page')
    if request.GET.get('Type'):
        Type = request.GET.get('Type')[:-1]
    try:
        goods_list = page_index(Goods, idv, Type)
        hot_goods = random.sample(list(Goods.objects.all()), 2)
        page_content = {'goods_list': goods_list, 'hot_goods' : hot_goods}
        # 页面上现实的上一页和下一页是被urlEncode转码的
    except DatabaseError as e:
        logging.warning(e)
    return render(request, 'list.html', {'content': page_content})


# 查找具体物品的详情页
def deatil_one(request):
    request.GET.getlist('')
    good_id = request.GET.get('good')[:-1]
    try:
        good = Goods.objects.get(id=good_id)
        good_type = good.type
        hot_good = good_type.goods_set.order_by('-id').all()[:2]
        # Typefood = GoodsType.objects.order_by(id='id')
        cart_count = 0
        # 判断是否处于session登录状态
        if request.session.get('user_id'):
            cart = CartInfo.objects.filter(user=request.session.get('user_id'))
            for i in cart:
                cart_count += 1
        # 判断商品是否在购物车当中
    except ObjectDoesNotExist as e:
        logging.warning(e)
    if request.COOKIES.get('Recently_Viewed'):
        cookie_good = request.COOKIES.get('Recently_Viewed')
        list_good = cookie_good.split(',')
        if good.id in list_good:
            list_good.remove(good.id)
        # 如果最近浏览多的话那么将最久没有被浏览的那个商品删除
        if len(list_good) >= 5:
            list_good.pop()
        list_good = [good_id] + list_good
        cookie_good_new = ','.join(list_good)
    else:
        cookie_good_new = good_id
    # cookie处理数据添加的位置
    response = render(request, 'detail.html', {'goodone': good, 'hot_list': hot_good, 'cart_count':cart_count})
    response.set_cookie('Recently_Viewed', cookie_good_new, max_age=3000)
    return response


# 好吧 如果有bug请尽快联系我 我负责(立Flag找时间)修~
def call_me(request):
    return render(request, 'contact_us.html')