from .models import Cart, AutoPart, CartContent
from django.shortcuts import get_object_or_404
from django.db.models import Q


class CartUser:
    """Корзина авторизованного пользователя"""

    def __init__(self, request):
        self.request = request
        self.cart = self.get_cart_auth_user(self.request)

    def add_to_cart(self, item):
        item_in_cart = CartContent.objects.filter(Q(object_id=item.pk) & Q(cart=self.cart)).first()
        if not item_in_cart:
            CartContent.objects.create(cart=self.cart, content_object=item)

    def get_final_price(self):
        """Итоговая цена"""
        return self.cart.get_total_price()

    def get_total_items(self):
        """Количество кроссовок"""
        return self.cart.get_cart_content_count()

    def __iter__(self):
        for item in self.cart.get_cart_content():
            yield {'id': item.pk, 'item': item.content_object}

    def delete_item(self, item_id):
        """Удалить кроссовки из корзины"""
        item = get_object_or_404(CartContent, pk=item_id)
        item.delete()

    def get_cart_auth_user(self, request: object):
        """Получить корзину пользователя"""
        if request.user.is_authenticated:
            user = request.user
            cart, create = Cart.objects.get_or_create(customer=user)
        return cart
