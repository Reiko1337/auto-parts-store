from .cart.cart_anonymous import CartSession
from .cart.cart_auth_user import CartUser


def get_cart_context(request):
    if request.user.is_authenticated:
        cart = CartUser(request)
        return {'cart': cart}
    else:
        cart = CartSession(request)
        return {'cart': cart}
