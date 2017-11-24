# python3
from django.conf.urls import url
from .models import *
from memberapp import views

# 局部的URL更新
urlpatterns = [
    url(r'^prolist/$', views.prolist_list, name='goodslist'),
    url(r'^detail/', views.deatil_one, name='detatil'),
]