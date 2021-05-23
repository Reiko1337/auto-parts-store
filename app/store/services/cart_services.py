from ..models import Cart
from ..session import CartSession
from ..services_auth_user import CartUser


def get_cart_auth_user(request):
    """Получить корзину пользователя"""
    if request.user.is_authenticated:
        user = request.user
        cart, create = Cart.objects.get_or_create(customer=user)
    return cart


def add_item_to_cart(request, item):
    if request.user.is_authenticated:
        cart = CartUser(request)
        result = cart.add_to_cart(item)
    else:
        cart = CartSession(request)
        result = cart.add_to_cart(item)
    return result


def delete_item_to_cart(request, model, item_id):
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.delete_item(item_id)
    else:
        cart = CartSession(request)
        cart.delete_item(model, item_id)
