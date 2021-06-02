import copy
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from ..session import Session


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
        item_model = str(item._meta.model_name)
        if not self.session['cart'].get(item_model):
            self.session['cart'][item_model] = {}
        if self.session['cart'][item_model].get(item_id) is None:
            self.session['cart'][item_model][item_id] = {}
            result = True
        else:
            result = False
        self.save()
        return result

    def __iter__(self):
        self.validation()
        for model in reversed(self.cart):
            for id in self.cart[model]:
                item_model = get_object_or_404(ContentType, model=model)
                item = get_object_or_404(item_model.model_class(), pk=id)
                yield {'id': item.pk, 'item': item}

    def get_final_price(self):
        """Итоговая цена"""
        self.validation()
        final_price = 0
        for model in reversed(self.cart):
            for id in self.cart[model]:
                item_model = get_object_or_404(ContentType, model=model)
                item = get_object_or_404(item_model.model_class(), pk=id)
                final_price += item.price
        return final_price

    def get_total_items(self):
        """Общее количество товаров"""
        self.validation()
        count = 0
        for model in reversed(self.cart):
            for _ in self.cart[model]:
                count += 1
        return count

    def delete_item(self, model, id):
        """Удалить товар из корзины"""
        if model in self.cart.keys():
            del self.cart[model][id]
            self.save()

    def validation(self):
        """Валидация товара"""
        cart = copy.deepcopy(self.cart)
        for model in cart:
            for id in cart[model]:
                item_model = get_object_or_404(ContentType, model=model)
                item = get_object_or_404(item_model.model_class(), pk=id)
                if not item.in_stock:
                    self.delete_item(model, id)
