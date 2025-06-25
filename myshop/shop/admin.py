from django.contrib import admin
from .models import *


#------------------------------------categories model------------------------------------
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('categoryid', 'name')
    list_editable = ('name',)
    list_per_page = 10
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.order_by('name')
    

    search_fields = ['name']
    list_filter = ['name']

#------------------------------------product model------------------------------------

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('productid', 'name', 'productcategory', 'price', 'stock')
    list_editable = ('price', 'stock')
    list_per_page = 10
    sortable_by = ('productid')

    def productcategory(self, obj):
        return obj.productcategory.name
    productcategory.short_description = 'Category'

    search_fields = ['name', 'description', 'productcategory__name']
    list_filter = ['productcategory__name']

#------------------------------------user register model------------------------------------
@admin.register(users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('userid', 'get_full_name', 'get_email', 'phone')
    list_per_page = 10

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'

    def get_email(self, obj):
        return obj.email
    get_email.short_description = 'Email'

    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    list_filter = ['user__email']



#------------------------------------wishlist model------------------------------------
@admin.register(wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlistid', 'get_username', 'productid')
    sortable_by = ('wishlistid')
    list_per_page = 10
    
   

    def get_username(self, obj):
        return obj.userid.username
    get_username.short_description = 'Username'

    search_fields = ['userid__username', 'productid']
    list_filter = ['userid__username']
#-------------------------------------banner model------------------------------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('bannerid', 'title', 'image')
    list_editable = ('title',) 
    list_per_page = 10
    sortable_by = ('bannerid')

    search_fields = ['title']
    list_filter = ['title']
#------------------------------------cart model------------------------------------
@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cartid', 'get_username', 'productid', 'quantity')
    sortable_by = ('cartid')
    list_per_page = 10

    def get_username(self, obj):
        return obj.userid.username
    get_username.short_description = 'Username'

    search_fields = ['userid__username', 'productid__name']
    list_filter = ['userid__username']
#------------------------------------order model------------------------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'get_username', 'totalbillamount', 'order_date')
    search_fields = ['userid__username']
    list_per_page = 10
    list_filter = ['order_date']

    def get_username(self, obj):
        return obj.userid.username
    get_username.short_description = 'Username'

#------------------------------------order item model------------------------------------
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):     
    list_display = ('orderitemid', 'get_orderid', 'productid', 'quantity', 'price')
    sortable_by = ('orderitemid')
    list_per_page = 10

    def get_orderid(self, obj):
        return obj.orderid.orderid
    get_orderid.short_description = 'Order ID'

    search_fields = ['orderid__orderid', 'productid__name']
    list_filter = ['orderid__order_date']
#---------------------place order model-----------------------------------------
@admin.register(PlaceOrder)
class PlaceOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phonenumber', 'ordertime', 'orders')
    list_display_links = ('name',)  # 'name' is in list_display
    list_filter = ('ordertime', 'name')
    ordering = ('-ordertime',)
    list_per_page = 20

    

  
