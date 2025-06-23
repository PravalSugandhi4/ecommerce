from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
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
    is_in_wishlist = False

    if request.user.is_authenticated:
        is_in_wishlist = wishlist.objects.filter(
            userid__user=request.user,
            productid=product
        ).exists()

    return render(request, 'shop/productdetail.html', {
        'product': product,
        'is_in_wishlist': is_in_wishlist
    })








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









def checkout(request):
    return render(request,"shop/checkout.html")




from django.http import HttpResponse

def addtowishlist(request, productid):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your wishlist.")
        return redirect('home')
    current_user = users.objects.get(user=request.user)
    product = Products.objects.get(productid=productid)

    if wishlist.objects.filter(userid=current_user, productid=product).exists():
        messages.info(request, "Already in wishlist")
    else:
        wishlist.objects.create(userid=current_user, productid=product)
        messages.success(request, "Item added to wishlist")
    return redirect('productdetail', myproductid=productid)


def removefromwishlist(request,productid):
        current_user = users.objects.get(user=request.user)
        product = Products.objects.get(productid=productid)
        wishlist_item = wishlist.objects.filter(userid=current_user, productid=product)
        if wishlist_item.exists():
            wishlist_item.delete()
            messages.success(request, "Item removed from wishlist")
        else:
            messages.error(request, "Item not found in wishlist")
        return redirect('wishlist')



def addtocart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('home')
    pass





def removefromcart(request):
    pass



def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('home')
    return render(request,'shop/cartpage.html')

def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')
