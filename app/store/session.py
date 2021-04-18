import copy
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import AutoPart


class Session:
    """Сессия"""

    def __init__(self, request):
        self.request = request
        self.session = request.session

    def save(self):
        self.session.modified = True


class CartSession(Session):
    """Корзина анонимного пользователя"""

    def __init__(self, request):
        super().__init__(request)

        if not self.session.get('cart'):
            self.session['cart'] = {}
        self.cart = self.session['cart']

    def add_to_cart(self, item):
        """Добавить в корзину"""
        self.validation()
        item_id = str(item.pk)
        if not self.session['cart'].get(item_id):
            self.session['cart'][item_id] = {}
        self.save()

    def __iter__(self):
        self.validation()
        for item_id in reversed(self.cart):
            item = get_object_or_404(AutoPart, Q(pk=item_id) & Q(in_stock=True))
            yield {'id': item.pk, 'item': item}

    def get_final_price(self):
        """Итоговая цена"""
        self.validation()
        return sum(get_object_or_404(AutoPart, pk=item_id).price for item_id in self.cart)

    def get_total_items(self):
        """Количество кроссовок"""
        self.validation()
        return len(self.cart.keys())

    def delete_item(self, item):
        """Удалить кроссовки из корзины"""
        item_id = str(item.pk)
        if item_id in self.cart.keys():
            del self.cart[item_id]
            self.save()

    def validation(self):
        cart = copy.deepcopy(self.cart)
        for item_id in cart:
            item = get_object_or_404(AutoPart, pk=item_id)
            if not item.in_stock:
                self.delete_item(item)
