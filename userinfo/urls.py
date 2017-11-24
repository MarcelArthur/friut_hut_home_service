# python3
from django.conf.urls import url,include
from django.contrib import admin
from userinfo import views


urlpatterns = [
    url(r'^login/', views.signin, name='login'),
    url(r'^register/', views.register_in, name='register'),
    url(r'^reigseterin/', views.register_, name='register_in'),
    url(r'^loginin/', views.login_, name='login_in'),
    url(r'^loginout/', views.login_out, name='login_out'),
    url(r'^info/$', views.user_info, name='user_info'),
    url(r'^address/', views.user_info_address, name='address'),
    url(r'^add_info/', views.user_info_address_add, name='address_add'),
    url(r'select_address/(\d+)/', views.select_address, name='selectaddress'),
    url(r'delete_address/(\d+)/', views.delete_address, name='deleteaddress'),
    url(r'^checkaddress/(\d+)/', views.checkaddress, name='checkaddress'),
    url(r'^updateaddress/(\d+)/', views.updateaddress, name='updateaddress'),
]