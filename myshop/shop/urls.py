from django.urls import path
from shop.views import *

urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('login/', userlogin, name='login'),
    path('product/<int:myproductid>/',productdetail, name='productdetail'),
    path('wishlist/', wishlist, name='wishlist'),
    path('checkout/', checkout, name='checkout'),
    path('logout/', logoutuser, name='logout'),   
]
