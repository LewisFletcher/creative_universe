from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ShippingAddress, Customer, Order, Price, Product
# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Price)
admin.site.register(Product)