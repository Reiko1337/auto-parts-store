from ..models import Cart
from ..cart.cart_anonymous import CartSession
from ..cart.cart_auth_user import CartUser


def get_cart_auth_user(request):
    """Получить корзину пользователя"""
    if request.user.is_authenticated:
        user = request.user
        cart, create = Cart.objects.get_or_create(customer=user)
    return cart


def add_item_to_cart(request, item):
    """Добавить в корзину"""
    if request.user.is_authenticated:
        cart = CartUser(request)
        result = cart.add_to_cart(item)
    else:
        cart = CartSession(request)
        result = cart.add_to_cart(item)
    return result


def delete_item_to_cart(request, model, item_id):
    """Удалить из корзины"""
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.delete_item(item_id)
    else:
        cart = CartSession(request)
        cart.delete_item(model, item_id)
