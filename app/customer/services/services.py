from ..models import AddressUser
from store.models import Order, OrderContent
from django.shortcuts import get_object_or_404
from django.db.models import Q


def get_addresses_user(request):
    """Список адресов доставки пользователя"""
    return AddressUser.objects.filter(user=request.user).all()


def get_address_user(request, id):
    """Адрес доставки"""
    return get_object_or_404(AddressUser, Q(pk=id) & Q(user=request.user))


def get_address_user_first(request, id):
    """Адрес доставки (AJAX)"""
    return AddressUser.objects.filter(Q(pk=id) & Q(user=request.user)).first()


def get_order_in_processes(queryset):
    """Текущие заказы"""
    return queryset.filter(status__in=['new', 'in_progress', 'is_ready']).all()


def get_orders_user(request):
    """Список заказов пользователя"""
    return Order.objects.filter(user=request.user).all()


def add_order_content(cart_content, order):
    """Оформление заказа (Добавление товара в заказ)"""
    for item in cart_content:
        OrderContent.objects.create(order=order, title=item.content_object.get_title(),
                                    price=item.content_object.get_price(), content_object=item.content_object)
        item.content_object.in_stock = False
        item.content_object.save()
        item.delete()