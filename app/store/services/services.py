from ..models import CarModel, CarBrand, Category, AutoPart, Cart, WheelDrive, Car, Bodywork, EngineType
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


def get_model_class(model):
    """Модель базы данных"""
    return get_object_or_404(ContentType, model=model)


def get_model_by_id(klass, id):
    """Записись таблицы модели по ID"""
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


def get_list_auto_part_for_detail(model_slug):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    return AutoPart.objects.filter(Q(car_model=car_model) & Q(in_stock=True)).all()


def get_similar_auto_parts(model_slug, category_slug, product):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    category = get_object_or_404(Category, slug=category_slug)
    return AutoPart.objects.filter(Q() & Q(car_model=car_model) & Q(in_stock=True) & Q(category=category)).exclude(
        pk=product.pk).all()


def get_similar_kit_cat(model_slug, product):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    return get_kit_car().filter(Q(car_model=car_model)).exclude(pk=product.pk).all()


def get_similar_wheel(model_slug, product):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    return get_wheel_drive().filter(car_model=car_model).exclude(pk=product.pk).all()


def get_kit_car():
    """Список машинокомплектов"""
    return Car.objects.filter(in_stock=True).all()


def get_list_kit_car_for_detail(model_slug):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    return get_kit_car().filter(Q(car_model=car_model)).all()


def get_kit_car_year():
    """Список годов машинокомплектов"""
    return get_kit_car().values('year').order_by('-year').distinct('year')


def get_kit_car_engine_capacity():
    """Список объемов двигателя машинокомплектов"""
    return get_kit_car().values('engine_capacity').order_by('-engine_capacity').distinct('engine_capacity')


def get_wheel_drive():
    """Список дисков"""
    return WheelDrive.objects.filter(in_stock=True).all()


def get_list_wheel_for_detail(model_slug):
    car_model = get_object_or_404(CarModel, slug=model_slug)
    return get_wheel_drive().filter(car_model=car_model).all()


def get_wheel_drive_material():
    """Список материалов диска"""
    return get_wheel_drive().values('material').order_by('-material').distinct('material')


def get_wheel_drive_pcd():
    """Список материалов диска"""
    return get_wheel_drive().values('pcd').order_by('-pcd').distinct('pcd')


def get_wheel_drive_diameter():
    """Список материалов диска"""
    return get_wheel_drive().values('diameter').order_by('-diameter').distinct('diameter')


def get_category():
    """Вернуть список категорий"""
    return Category.objects.all()


def get_wheel_drive_by_id(id):
    return get_object_or_404(WheelDrive, pk=id)


def get_auto_part_by_id(id):
    return get_object_or_404(AutoPart, pk=id)
