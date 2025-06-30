from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


#------------------------------------user register view------------------------------------
def index(request):
    products = Products.objects.all()
    banners = Banner.objects.all()
    if not request.user.is_authenticated:
        return render(request, 'shop/index.html',{'banners': banners,'products': products})

   
    current_user = users.objects.get(user=request.user)
    stockproducts = [product for product in products if product.stock <=0]
    cart_product_ids = []
    cart_product_ids = cart.objects.filter(userid=current_user).values_list('productid__productid', flat=True)
    return render(request, 'shop/index.html', {'banners': banners,'products': products, 'stockproducts': stockproducts,'cart_product_ids': list(cart_product_ids)})




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
    banners = Banner.objects.all()
    if not request.user.is_authenticated:
        return render(request, 'shop/homepage.html',{'banners': banners,'products': products})

   
    current_user = users.objects.get(user=request.user)
    stockproducts = [product for product in products if product.stock <=0]
    cart_product_ids = []
    cart_product_ids = cart.objects.filter(userid=current_user).values_list('productid__productid', flat=True)
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


    if not products:
        messages.info(request, "Your wishlist is empty.")
    else:
        messages.success(request, "Here are your wishlist items.")

    return render(request, "shop/wishlist.html", {'products': products})


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
        return redirect('viewcart')  # Redirect to view cart or wherever appropriate
    else:
        # Create a new cart item
        cart.objects.create(userid=current_user, productid=product, quantity=1)
        messages.success(request, "Item added to cart")    
        return redirect('home')  # Redirect to home or wherever appropriate
    

def removefromcart(request, productid):

    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to remove items from your cart.")
        return redirect('home')
    # Implement the logic to remove items from the cart
    current_user = users.objects.get(user=request.user)
    product = Products.objects.get(productid=productid)
    try:
        cart_item = cart.objects.get(userid=current_user, productid=product)
        cart_item.delete()
        messages.success(request, "Item removed from cart")
    except cart.DoesNotExist:
        messages.error(request, "Item not found in cart")
    return redirect('viewcart')  # Redirect to view cart or wherever appropriate
    #   


def viewcart(request):

    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('home')
    current_user = users.objects.get(user=request.user)
    cartitems = cart.objects.filter(userid=current_user)
    products = [item.productid for item in cartitems]
    total_items=0
    subtotal=0
    if not products:
        messages.info(request, "Your cart is empty.")
        total_items=0
        subtotal=0
    else:
        messages.success(request, "Here are your cart items.")
        total_items = sum(item.quantity for item in cartitems)
        subtotal = sum(item.quantity * item.productid.price for item in cartitems)
       
    return render(request,'shop/cartpage.html', {'products': products, 'cartitems': cartitems,'total_items':total_items,'subtotal':subtotal})


def updatecart(request, productid):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to update your cart.")
        return redirect('login')  # Consider redirecting to login

    if request.method == "POST":
        try:
            current_user = users.objects.get(user=request.user)
            product = Products.objects.get(productid=productid)
            cart_item = cart.objects.get(userid=current_user, productid=product)

            new_quantity = int(request.POST.get('quantity', 1))

            if new_quantity <= 0:
                cart_item.delete()
                messages.success(request, "Item removed from cart.")
            else:
                cart_item.quantity = min(new_quantity, 5)  # Optional: cap at 5
                messages.success(request, "Item quantity updated.")
                cart_item.save()
                
                
        except (cart.DoesNotExist, Products.DoesNotExist):
            messages.error(request, "Item not found in cart.")

    return redirect('viewcart')


    
def checkout(request):
    current_user = users.objects.get(user=request.user)
    cartitems = cart.objects.filter(userid=current_user)

    if not cartitems:
        messages.error(request, "Your cart is empty.")
        return redirect('viewcart')

    subtotal = sum(item.productid.price * item.quantity for item in cartitems)
    deliverytax=150
    totalbillamount=subtotal+deliverytax

    return render(request, 'shop/checkout.html', {
        'cartitems': cartitems,
        'subtotal': subtotal,
        'deliverytax':deliverytax,
        'totalbillamount':totalbillamount
    })
    

def placeorder(request):
    from django.contrib import messages
from django.shortcuts import redirect, render
from django.db import transaction
from .models import cart, Order, OrderItem, PlaceOrder, Products, users


@transaction.atomic
def placeorder(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to login first.")
        return redirect('home')

    try:
        user_profile = users.objects.get(user=request.user)
    except users.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('home')

    if request.method == 'POST':
        cartitems = cart.objects.filter(userid=user_profile)

        if not cartitems.exists():
            return render(request, 'shop/orderfail.html', {
                'message': "⚠️ Your cart is empty. Cannot place an order."
            })

        name = request.POST.get('fullname')
        address = request.POST.get('address')
        phonenumber = request.POST.get('phone')

              # Check stock for all items
        insufficient_stock_items = []
        for item in cartitems:
            if item.quantity > item.productid.stock:
                insufficient_stock_items.append({
                    'name': item.productid.name,
                    'available': item.productid.stock,
                    'requested': item.quantity
                })

        if insufficient_stock_items:
            return render(request, 'shop/orderfail.html', {
                'message': "Some products are out of stock.",
                'insufficient_items': insufficient_stock_items
            })

           

        # Create order and items
        total_amount = sum(item.quantity * item.productid.price for item in cartitems)
        order = Order.objects.create(userid=user_profile, totalbillamount=total_amount)

        for item in cartitems:
            OrderItem.objects.create(
                orderid=order,
                productid=item.productid,
                quantity=item.quantity,
                price=item.productid.price
            )
            item.productid.stock -= item.quantity
            item.productid.save()

        PlaceOrder.objects.create(
            name=name,
            address=address,
            phonenumber=phonenumber,
            orders=order
        )

        cartitems.delete()

        return render(request, 'shop/ordersucess.html', {'order': order,'total': total_amount})

    return redirect('viewcart')




def logoutuser(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


def pastorders(request):
    if not request.user.is_authenticated:
        return redirect('home')

    try:
        user_profile = users.objects.get(user=request.user)
    except users.DoesNotExist:
        return redirect('home')

    orders = Order.objects.filter(userid=user_profile).order_by('-order_date')

    # Prepare a list of orders with their items
    order_data = []
    for order in orders:
        items = OrderItem.objects.filter(orderid=order)
        order_data.append({
            'order': order,
            'items': items
        })

    return render(request, 'shop/orderhistory.html', {
        'order_data': order_data
    })
