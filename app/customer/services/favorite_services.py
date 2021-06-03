from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ..models import Favorite


def product_is_favorite(item, user):
    """Товар есть в списке избранных или нет"""
    if user.is_authenticated:
        if item.favorite.filter(user=user):
            return True
    return False


def favorite_add(item, user):
    """Добавить в избранное"""

    model = ContentType.objects.get_for_model(item)
    item_in_cart = Favorite.objects.filter(Q(user=user) &
                                           Q(object_id=item.pk) & Q(content_type=model)).first()
    if not item_in_cart:
        Favorite.objects.create(user=user, content_object=item)
        return True


def favorite_delete(item, user):
    """Удалить товар из избранных"""
    model = ContentType.objects.get_for_model(item)
    item = get_object_or_404(Favorite, Q(object_id=item.pk) & Q(user=user) & Q(content_type=model))
    item.delete()


def get_favorite_products(favorite_user, model_db):
    """Избранный список товаров"""
    content_type = ContentType.objects.get_for_model(model_db)
    favorite = favorite_user.filter(content_type=content_type).all().values('object_id')
    return model_db.objects.filter(pk__in=favorite)
