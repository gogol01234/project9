from django.contrib import admin
from app1.models import Customer, OrderedPlaced, Product, Cart
# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderedPlaced)