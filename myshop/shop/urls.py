from django.urls import path
from shop.views import *

urlpatterns = [
    path('',home, name='home'),
    path('register/', register, name='register'),
    path('login/', userlogin, name='login'),
    path('product/<int:myproductid>/',productdetail, name='productdetail'),
    path('wishlist/', userwishlist, name='wishlist'),
    path('checkout/', checkout, name='checkout'),
    path('logout/', logoutuser, name='logout'),  
    path('cart/', viewcart, name='viewcart'), 
    path('addtocart/<int:productaddtocart>/', addtocart, name='addtocart'),
    path('addtowishlist/<int:productid>/', addtowishlist, name='addtowishlist'),
    path('removefromwishlist/<int:productid>/', removefromwishlist, name='removefromwishlist'),
    path('updatecart/<int:productid>/', updatecart, name='updatecart'),
    path('removefromcart/<int:productid>/', removefromcart, name='removefromcart'),
    path('placeorder/',placeorder,name='placeorder'),
    path('pastorders/',pastorders,name='pastorders'),
   
   

    
]
