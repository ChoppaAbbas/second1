from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddShoesForm
from django.contrib.auth import authenticate, login
from shop.models import Shoes, Order
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('products')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('products')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)

        return redirect('products')
    else:
        return render(request, 'register.html')


def products(request):
    shoes = Shoes.objects.all()
    return render(request, "products.html", context={"shoes": shoes})



@login_required
def add_to_cart(request, id):
    shoe = get_object_or_404(Shoes, pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart.shoes.add(shoe)
    cart.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    shoe = get_object_or_404(Shoes, pk=id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.shoes.remove(shoe)
    messages.success(request, f"{shoe.title} has been removed from your cart.")
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        shoe_id = request.POST.get('id')
        if shoe_id:
            shoe = get_object_or_404(Shoes, pk=shoe_id)
            cart.shoes.remove(shoe)
            cart.save()

    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)


def buy(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        order = Order.objects.create(name=name, email=email, phone=phone, user=request.user, cart=Cart.objects.get(user=request.user))
        print(order)
        return redirect('processed')

    return render(request, "buy.html")


def processed(request):
    return render(request, "processed.html")


def about(request):
    return render(request, "about.html")