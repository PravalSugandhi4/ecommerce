from django.db import models

# Create your models here.
class Categories(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
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

