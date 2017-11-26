from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import request, response, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Permission
from django.db import DatabaseError
import logging
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from memberapp.models import Goods
# Create your views here.
from hashlib import sha1
from memberapp.views import expire_page
# get请求
auth_check = 'MarcelArhut'


# 重定向非法的注册和登录请求
def rendirct_decorator(func):
    def rendirct_login_regsiter(request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('/')
        return func(request, *args, **kwargs)
    return rendirct_login_regsiter


# 装饰器(面向切面， 对于某些页面进行装饰， 要求进行权限认证, 并且记录跳转前的位置值)
def login_decorator(func):
    def login_func(request, *args, **kwargs):
        # if request.session.get('user_id', None):...
        if request.session.get('user_name', None):
            return func(request, *args, **kwargs)
        else:
            response = redirect('/user/login/')
            response.set_cookie('url', request.path)
            return response
    return login_func

# 清除Cookies中的数据转存到Session中(购物车啊)


# 拦截器2 如果已经登录过那么首先跳转到原页面 或者跳转到原有的页面


# 重定向到登录页
@rendirct_decorator
def signin(request):
    return render(request, 'login.html')


# 重定向到注册页面
@rendirct_decorator
def register_in(request):
    return render(request, 'register.html')


# 处理post请求页面，如果完成重新跳转到对应的页面

def login_(request):
    if request.method == 'POST':
        user = UserInfo()
        user.uname = request.POST.get('username')
        user.upassword = request.POST.get('pwd')
        try:
            find_user = UserInfo.objects.filter(uname=user.uname)
            if len(find_user) <= 0:
                messages.add_message(request, messages.ERROR, '该用户未注册')
                return redirect('/user/login/')
            if not check_password(user.upassword, find_user[0].upassword): #
                return render(request, 'login.html', {'user_info': user, 'message_error': '用户名或者密码错误'})
        except ObjectDoesNotExist as e:
            logging.warning(e)
        request.session['user_id'] = find_user[0].id
        request.session['user_name'] = user.uname
        request.session.set_expiry(30 * 60)
        if request.COOKIES.get('url'):
            url = request.COOKIES.get('url')
            res = redirect(url)
            res.delete_cookie('url')
            return res
        # 购物车的中的数据清空并转存到session当中
        # if request.COOKIES.get('cart'):
        #       request.session['cart'] = request.COOKIES.get('cart')
        #       del request.COOKIES['cart']
        expire_page('index', request)
        return redirect('/')
    return redirect('/user/login/')


def register_(request):
    if request.method == 'POST':
        new_user = UserInfo()
        new_user.uname = request.POST.get('user_name')
        try:
            a = UserInfo.objects.get(uname=new_user.uname)
            if a:
                return render(request, 'register.html', {'messageuname': '该用户名已经存在'})
        except BaseException as e:
            logging.warning(e)
        if request.POST.get('pwd') != request.POST.get('cpwd'):
            return render(request, 'register.html', {'message_': '两次输入的密码不一致'})
        new_user_pwd = make_password(request.POST.get('pwd'), auth_check, 'pbkdf2_sha1')
        new_user.upassword = new_user_pwd
        new_user.email = request.POST.get('email')
        try:
            new_user.save()
        except DatabaseError as e:
            logging.warning(e)
        return render(request, 'loading.html')
    return redirect('/user/register/')


# 处理的页面信息
def login_out(request):
    try:
        if request.session['user_name']:
            del request.session['user_id']
            del request.session['user_name']
        expire_page('index', request)
    except KeyError as e:
        logging.warning(e)
    return redirect('/')


# 会员中心的数据, 同时有权限认证
@login_decorator
def user_info(request):
    try:
        rec_view_list = list()
        userinfo = get_object_or_404(UserInfo, uname=request.session.get('user_name'))
        if request.COOKIES.get('Recently_Viewed', None):
            rec_view = request.COOKIES.get('Recently_Viewed', None)
            list_view = rec_view.split(',')
            for i in list_view:
                rec_view_list.append(Goods.objects.get(id=i))
        else:
            rec_view_list = []
    except ObjectDoesNotExist as e:
        logging.warning(e)
    content = {'userinfo': userinfo, 'rec_view': rec_view_list}
    return render(request, 'user_center_info.html', content)


# 显示所有的邮寄地址
@login_decorator
def user_info_address(request):
    user_id = request.session.get('user_id')
    add_len = Address.objects.filter(user=user_id)
    if len(add_len) > 0:
        content_add = {'add_list': add_len}
    else:
        content_add = {'add_list': add_len, 'no_add': '显然什么都没有， 快点添加收货地址， 买买买啊'}
    return render(request, 'user_center_site.html', content_add)


def user_info_address_add(request):
    if request.method == 'POST':
        a_user_id = request.session.get('user_id')
        user = UserInfo.objects.get(id=a_user_id)
        __address = Address()
        __address.user = user
        __address.aname = request.POST.get('addressee')
        __address.address = request.POST.get('Detailed_address')
        __address.PostalCode = request.POST.get('address')
        __address.cellphone = request.POST.get('cellphone')
        try:
            __address.save()
        except DatabaseError as g:
            logging.warning(g)
            raise '服务器异常，插入失败'
        except BaseException as e:
            logging.warning(e)

        # address_list = serializers.serialize('json', Address.objects.filter(user=a_user_id))
        # # 这里应该返回一个符合RESTful标准的状态码
        # return HttpResponse(address_list)
        return redirect('/user/address/')
    return redirect('/user/address/')


def select_address(request, id):
    active_address = Address.objects.filter(isactive=True)
    if len(active_address) > 0:
        active_address[0].isactive = False
        active_address[0].save()
    address = Address.objects.filter(id=id)
    if len(address) > 0:
        address[0].isactive = True
        address[0].save()
    return redirect('/user/address/')


def delete_address(request, id):
    active = Address.objects.filter(id=id).delete()
    return redirect('/user/address/')

# 更新当前地址的数据


# 如果改为get请求访问页面则可以放弃这段代码实现复用
def checkaddress(request, id):
    user_id = request.session.get('user_id')
    add_all = Address.objects.filter(user=user_id)
    old_address = Address.objects.filter(id=id)
    if len(old_address) > 0:
        return render(request, 'user_center_site.html', {'edit_address': old_address[0], 'add_list': add_all})
    return redirect('/user/address/')


# 好吧更新数据 感觉又重复了一次代码 囧
def updateaddress(request, id):
    new_address = Address.objects.filter(id=id)
    if len(new_address) > 0 and request.method == 'POST':
        new_address = new_address[0]
        new_address.aname = request.POST.get('addressee')
        new_address.address = request.POST.get('Detailed_address')
        new_address.PostalCode = request.POST.get('address')
        new_address.cellphone = request.POST.get('cellphone')
        try:
            new_address.save()
        except BaseException as e:
            logging.warning(e)
    return redirect('/user/address/')