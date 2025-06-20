from django.urls import path
from shop.views import *

urlpatterns = [
    path('',home, name='home'),
    path('product/<int:myproductid>/',productdetail, name='productdetail'),
    path('wishlist/', wishlist, name='wishlist'),
    
]
