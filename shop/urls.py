from django.urls import path
from shop.views import user_login, register, products, add_to_cart, cart, buy, user_logout, processed, about, remove_from_cart

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('', products, name='products'),
    # path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    # path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    # path('cart/', cart, name='cart'),
    # path('cart/buy/', buy, name='buy'),
    # path("processed/", processed, name="processed"),
    path("about/", about, name="about")
]
