from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib import admin
from django.utils import timezone

#------------------------------------banner model------------------------------------
class Banner(models.Model):
    bannerid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='myshop/media/', null=True, blank=True)

    def __str__(self):
        return self.title


#------------------------------------user register model------------------------------------



class users(models.Model):
    userid = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    username = models.CharField(max_length=50, unique=True, default="")
    email = models.EmailField(unique=True, default="")
    password = models.CharField(max_length=100, default="")  # Optional: store masked or leave blank
    phone = models.CharField(max_length=15, null=True, blank=True, default="")

    def __str__(self):
        return self.username

#------------------------------------categories model------------------------------------

class Categories(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name








#------------------------------------products model------------------------------------
class Products(models.Model):

    productid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    productcategory = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    productimage = models.ImageField(upload_to='shop/media/', null=True, blank=True)


    def __str__(self):
        return f"{self.productid} - {self.name}"



#------------------------------------wishlist model------------------------------------
    
class wishlist(models.Model):
    wishlistid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(users, on_delete=models.CASCADE)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.userid.username} "
#-------------------------------------cart model------------------------------------
class cart(models.Model):
    cartid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(users, on_delete=models.CASCADE)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.userid.username} - {self.productid.name} ({self.quantity})"
#------------------------------------order model------------------------------------
class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(users, on_delete=models.CASCADE)
    totalbillamount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)    


    def __str__(self):
        return f"Order {self.orderid} by {self.userid.username}"
    

#------------------------------------order item model------------------------------------
class OrderItem(models.Model):
    orderitemid = models.AutoField(primary_key=True)
    orderid = models.ForeignKey(Order, on_delete=models.CASCADE)
    productid = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.orderid.orderid} - {self.productid.name} ({self.quantity})"
    
#-----------------------------place order-------------------------------------------------

class PlaceOrder(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    phonenumber = models.CharField(max_length=10)
    ordertime = models.DateTimeField(auto_now_add=True)
    orders = models.ForeignKey(Order, on_delete=models.CASCADE)






    








    