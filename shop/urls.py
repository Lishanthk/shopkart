
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[
    path('', views.home,name='home'),
    path('register', views.register,name='register'),
    path('collections', views.collections,name='collections'),
    path('collections/<str:name>', views.collectionsview,name='collections'),
     path('collections/<str:cname>/<str:pname>', views.prodetails,name='prodetails'),
    path('login', views.login_page,name='login'),
    path('logout', views.logout_page,name='logout'),
    path('cart', views.cart_page,name='cart'),
    path('addtocart', views.add_to_cart,name='addtocart'),
    path('remove_cart/<str:id>', views.remove_cart,name='remove_cart'),

]
