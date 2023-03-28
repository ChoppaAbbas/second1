from decimal import Decimal
from django.conf import settings
from shop.models import Clothes


class Cart(object):
    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        shoes_id = str(product.id)
        if shoes_id not in self.cart:
            self.cart[shoes_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[shoes_id]['quantity'] = quantity
        else:
            self.cart[shoes_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, shoes):
        """Удаление товара из корзины."""
        shoes_id = str(shoes.id)
        if shoes_id in self.cart:
            del self.cart[shoes_id]
            self.save()

    def __iter__(self):
        shoes_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        shoes = Clothes.objects.filter(id__in=shoes_ids)
        cart = self.cart.copy()
        for s in shoes:
            cart[str(s.id)]['product'] = s
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values())

    def clear(self):
        # Очистка корзины.
        del self.session['cart']
        self.save()
