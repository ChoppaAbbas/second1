from django.contrib import admin
from shop.models import Shoes, Category, Cart, Order

admin.site.register(Shoes)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)