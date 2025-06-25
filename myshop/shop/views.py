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
    current_user = users.objects.get(user=request.user)
    products = Products.objects.all()
    cart_product_ids = cart.objects.filter(userid=current_user).values_list('productid__productid', flat=True)
    banners = Banner.objects.all()
    stockproducts = [product for product in products if product.stock <=0]
    cart_product_ids = []
    return render(request, 'shop/homepage.html', {'banners': banners,'products': products, 'stockproducts': stockproducts,'cart_product_ids': list(cart_product_ids)})

  







def productdetail(request, myproductid):  
    cart_product_ids = []
    product = Products.objects.get(productid=myproductid)
    products = Products.objects.all()
    stockproducts = [product for product in products if product.stock <=0]
    is_in_wishlist = False

    if request.user.is_authenticated:

        current_user = users.objects.get(user=request.user)
        cart_product_ids = cart.objects.filter(userid=current_user).values_list('productid__productid', flat=True)
        is_in_wishlist = wishlist.objects.filter(
            userid__user=request.user,
            productid=product
        ).exists()



    return render(request, 'shop/productdetail.html', {
        'product': product,
        'is_in_wishlist': is_in_wishlist,
        'stockproducts': stockproducts,
        'cart_product_ids': list(cart_product_ids)

    })




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



def addtocart(request,productaddtocart):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to add items to your cart.")
        return redirect('home')
    # Implement the logic to add items to the cart
    current_user = users.objects.get(user=request.user)
    product = Products.objects.get(productid=productaddtocart)
    # Check if the product is already in the cart
    if cart.objects.filter(userid=current_user, productid=product).exists():
        messages.info(request, "Item already in cart")
    else:
        # Create a new cart item
        cart.objects.create(userid=current_user, productid=product, quantity=1)
        messages.success(request, "Item added to cart")    
    return redirect('home')  # Redirect to home or wherever appropriate
    







def removefromcart(request):
    pass



def viewcart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('home')
    current_user = users.objects.get(user=request.user)
    cartitems = cart.objects.filter(userid=current_user)
    products = [item.productid for item in cartitems]
    if not products:
        messages.info(request, "Your cart is empty.")
    else:
        messages.success(request, "Here are your cart items.")
        print(cartitems)
    return render(request,'shop/cartpage.html', {'products': products, 'cartitems': cartitems})

def updatecart(request):
    pass
    


def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')
