# python3
from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^createorder/', views.create_order),
    url(r'^orderlist/', views.order_all, name='order_list'),
]