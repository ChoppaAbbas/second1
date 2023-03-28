from django.contrib import admin
from shop.models import Clothes, Category, Cart, Order

admin.site.register(Clothes)
admin.site.register(Category)
# admin.site.register(Cart)
admin.site.register(Order)
