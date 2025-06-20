from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib import admin
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
    




#------------------------------------wishlist model------------------------------------
    
class wishlist(models.Model):
    wishlistid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(users, on_delete=models.CASCADE)
    productid = models.IntegerField()

    def __str__(self):
        return f"Wishlist {self.wishlistid} for User {self.userid.username}"




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

    