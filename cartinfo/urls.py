# python3
from django.conf.urls import url
from cartinfo import views

urlpatterns= [
    url('^$', views.cart_info, name='cart'),
    url('^addcart/', views.add_cart),
    url(r'^updatecart/(\d+)/', views.update_cart),
    url(r'^placeorder/', views.create_place_order),
    url(r'^deletecart/', views.delete_cart, name='de_cart'),
]
