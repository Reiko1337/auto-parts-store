from .models import CarModel, CarBrand, Category, AutoPart, Cart, WheelDrive, Car, Bodywork, EngineType
from django.shortcuts import get_object_or_404
from .session import CartSession
from .services_auth_user import CartUser
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


def get_model_class(model):
    return get_object_or_404(ContentType, model=model)


def get_model_by_id(klass, id):
    return get_object_or_404(klass.model_class(), pk=id)


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


def get_wheel_drive_by_id(id):
    return get_object_or_404(WheelDrive, pk=id)


def get_auto_part_by_id(id):
    return get_object_or_404(AutoPart, pk=id)


def get_auto_parts_filter(brand, model, part):
    """Вернуть список запчастей по фильтрации (AJAX)"""
    brand_slug = brand
    model_slug = model
    part_slug = part

    if brand_slug:
        car_brand = CarBrand.objects.filter(slug=brand_slug).first()
        if model_slug:
            if model_slug:
                car_model = CarModel.objects.filter(slug=model_slug).all()
            else:
                car_model = CarModel.objects.filter(car_brand=car_brand).all()
            auto_part = AutoPart.objects.filter(car_model__in=car_model)
        else:
            car_model = CarModel.objects.filter(car_brand=car_brand).all()
            auto_part = AutoPart.objects.filter(car_model__in=car_model)
    else:
        auto_part = AutoPart.objects.all()

    if part_slug:
        category = Category.objects.filter(slug=part_slug).first()
        auto_part = auto_part.filter(category=category).all()
    return auto_part.filter(in_stock=True).all()


def get_wheel_drive_filter(brand, model, diameter, material, pcd):
    brand_slug = brand
    model_slug = model
    diameter = diameter
    material = material
    pcd = pcd

    if brand_slug:
        car_brand = CarBrand.objects.filter(slug=brand_slug).first()

        if model_slug:
            if model_slug:
                car_model = CarModel.objects.filter(slug=model_slug).all()
            else:
                car_model = CarModel.objects.filter(car_brand=car_brand).all()
            wheel_drive = WheelDrive.objects.filter(car_model__in=car_model)
        else:
            car_model = CarModel.objects.filter(car_brand=car_brand).all()
            wheel_drive = WheelDrive.objects.filter(car_model__in=car_model)
    else:
        wheel_drive = WheelDrive.objects.all()

    wheel_drive = wheel_drive.filter(
        Q(diameter__icontains=diameter) & Q(material__icontains=material) & Q(pcd__icontains=pcd))
    return wheel_drive.filter(in_stock=True).all()


def get_kid_car_filter(brand, model, transmission, bodywork, engine_type, drive):
    brand_slug = brand
    model_slug = model
    transmission = transmission
    bodywork = bodywork
    engine_type = engine_type
    drive = drive

    if brand_slug:
        car_brand = CarBrand.objects.filter(slug=brand_slug).first()

        if model_slug:
            if model_slug:
                car_model = CarModel.objects.filter(slug=model_slug).all()
            else:
                car_model = CarModel.objects.filter(car_brand=car_brand).all()
            car = Car.objects.filter(car_model__in=car_model)
        else:
            car_model = CarModel.objects.filter(car_brand=car_brand).all()
            car = Car.objects.filter(car_model__in=car_model)
    else:
        car = Car.objects.all()

    if bodywork:
        bodywork = Bodywork.objects.filter(slug=bodywork).all()
    else:
        bodywork = Bodywork.objects.all()
    if engine_type:
        engine_type = EngineType.objects.filter(slug=engine_type).all()
    else:
        engine_type = EngineType.objects.all()

    car = car.filter(
        Q(transmission__icontains=transmission) & Q(drive__icontains=drive) & Q(bodywork__in=bodywork) & Q(
            engine_type__in=engine_type))
    return car.filter(in_stock=True).all()


def get_car_models_filter(brand):
    """Вернуть список моделей автомобилей (AJAX)"""
    brand_slug = brand
    car_brand_first = CarBrand.objects.filter(slug=brand_slug).first()
    queryset = CarModel.objects.filter(car_brand=car_brand_first).all().values('title', 'slug')
    return queryset


def get_cart_auth_user(request):
    """Получить корзину пользователя"""
    if request.user.is_authenticated:
        user = request.user
        cart, create = Cart.objects.get_or_create(customer=user)
    return cart


def add_item_to_cart(request, item):
    # item = get_object_or_404(AutoPart, Q(id=item_id) & Q(in_stock=True))
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.add_to_cart(item)
    else:
        cart = CartSession(request)
        cart.add_to_cart(item)


def delete_item_to_cart(request, model, item_id):
    if request.user.is_authenticated:
        cart = CartUser(request)
        cart.delete_item(item_id)
    else:
        cart = CartSession(request)
        cart.delete_item(model, item_id)
