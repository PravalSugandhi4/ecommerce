from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


#------------------------------------user register view------------------------------------


from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import users  # your custom model
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email').lower()
        password = request.POST.get('password2')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('home')

        user_obj = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        users.objects.create(
            user=user_obj,
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password,
            phone=phone
        )

        login(request, user_obj)
        messages.success(request, "Registered and logged in successfully")
        return redirect('home')  # ✅ Refresh session
    return redirect('home')











def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')  # ✅ Use redirect instead of render
        else:
            messages.error(request, "Invalid credentials")
            return redirect('home')  # ✅ Triggers modal via JS logic

    return redirect('home')









def home(request):
    products = Products.objects.all()
    return render(request, 'shop/homepage.html', {'products': products})






def productdetail(request, myproductid):  
    product = Products.objects.get(productid=myproductid)
    return render(request, 'shop/productdetail.html', {'product': product})







from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import users, wishlist


def userwishlist(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your wishlist.")
        return redirect('home')
    
    custom_user = users.objects.get(user=request.user)
    wishlist_items = wishlist.objects.filter(userid=custom_user)
    products = [item.productid for item in wishlist_items]
    for product in products:
        print("Product name:", product.name)

    if not products:
        messages.info(request, "Your wishlist is empty.")
    else:
        messages.success(request, "Here are your wishlist items.")

    return render(request, "shop/wishlist.html", {'products': products})








@login_required
def checkout(request):
    return render(request,"shop/checkout.html")



@login_required
def addtowishlist(request):
    pass


@login_required
def removefromwishlist(request):
    pass


@login_required
def addtocart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('home')
    pass


@login_required
def removefromcart(request):
    pass


@login_required
def cart(request):
    pass

def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')
