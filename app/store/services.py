from .models import CarModel, CarBrand, Category, AutoPart, Cart
from django.shortcuts import get_object_or_404
from .session import CartSession
from .services_auth_user import CartUser
from django.db.models import Q

def get_cart_brand():
    """Вернуть марку автомобилей"""
    return CarBrand.objects.all()


def get_cart_brand_by_slug(slug):
    """Вернуть марку автомобилей по SLUG"""
    return CarBrand.objects.filter(slug=slug).first()


def get_cart_model():
    """Вернуть модель автомобилей"""
    return CarModel.objects.all()


def get_cart_model_by_brand_slug(car_brand_slug):
    """Вернуть модель автомобилей по SLUG марки автомобиля"""
    car_brand = get_cart_brand_by_slug(car_brand_slug)
    return CarModel.objects.filter(car_brand=car_brand)


def get_category():
    """Вернуть список категорий"""
    return Category.objects.all()


def get_auto_parts_filter(request):
    """Вернуть список запчастей по фильтрации (AJAX)"""
    brand_slug = request.GET.get('brand')
    model_slug = request.GET.get('model')
    part_slug = request.GET.get('part')

    if brand_slug and brand_slug != '*':
        car_brand = CarBrand.objects.filter(slug=brand_slug).first()

        if model_slug:
            if model_slug == '*':
                car_model = CarModel.objects.filter(car_brand=car_brand).all()
            else:
                car_model = CarModel.objects.filter(slug=model_slug).all()
            auto_part = AutoPart.objects.filter(car_model__in=car_model)
        else:
            car_model = CarModel.objects.filter(car_brand=car_brand).all()
            auto_part = AutoPart.objects.filter(car_model__in=car_model)
    else:
        auto_part = AutoPart.objects.all()

    if part_slug and part_slug != '*':
        category = Category.objects.filter(slug=part_slug).first()
        auto_part = auto_part.filter(category=category).all()
    return auto_part


def get_car_models_filter(request):
    """Вернуть список моделей автомобилей (AJAX)"""
    brand_slug = request.GET.get('brand')
    car_brand_first = CarBrand.objects.filter(slug=brand_slug).first()
    queryset = CarModel.objects.filter(car_brand=car_brand_first).all().values('title', 'slug')
    return queryset


def get_cart_auth_user(request):
    """Получить корзину пользователя"""
    if request.user.is_authenticated:
        user = request.user
        cart, create = Cart.objects.get_or_create(customer=user)
    return cart


def add_item_to_cart(request, item_id):
    item = get_object_or_404(AutoPart, Q(id=item_id) & Q(in_stock=True))
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.add_to_cart(item)
    else:
        cart = CartSession(request)
        cart.add_to_cart(item)


def delete_item_to_cart(request, item_id):
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.delete_item(item_id)
    else:
        item = get_object_or_404(AutoPart, Q(id=item_id) & Q(in_stock=True))
        cart = CartSession(request)
        cart.delete_item(item)
