from django.shortcuts import render
from django.http import HttpResponse
from .models import Products

def home(request):
    products = Products.objects.all()
    return render(request, 'shop/homepage.html', {'products': products})

def productdetail(request, myproductid):  
    product = Products.objects.get(productid=myproductid)
    return render(request, 'shop/productdetail.html', {'product': product})

def wishlist(request):
    return render(request,"shop/wishlist.html")
