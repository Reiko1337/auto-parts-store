from ..models import Model as ModelProduct, Brand, Category, SparePart, Tire, Wheel, KitCar, Bodywork, EngineType, \
    Manufacturer, Exchange
from django.db.models import Q
from .services import *


def get_filter_fields(request, kwargs=None):
    """Поля фильтрации"""
    fields = dict()
    if kwargs:
        for key, value in kwargs.items():
            fields[key] = value
    for key, value in request.GET.items():
        fields[key] = value

    return fields


def filter_brand_and_model(model_db, brand_slug, model_slug):
    """Фильтр по марке и модели автомобиля"""
    if brand_slug:
        brand = Brand.objects.filter(slug=brand_slug).first()
        if model_slug:
            if model_slug:
                model = ModelProduct.objects.filter(slug=model_slug).all()
            else:
                model = ModelProduct.objects.filter(brand=brand).all()
            list_products = model_db.objects.filter(model__in=model).all()
        else:
            model = ModelProduct.objects.filter(brand=brand).all()
            list_products = model_db.objects.filter(model__in=model).all()
    else:
        list_products = model_db.objects.all()

    return list_products


def price_filter_validation(list_products, price_from, price_to):
    """Фильтр по цене"""
    try:
        price_from = round(float(price_from), 2)
    except ValueError:
        price_from = ''

    try:
        price_to = round(float(price_to), 2)
    except ValueError:
        price_to = ''

    exchange = Exchange.objects.first()

    if price_from and price_to:
        if exchange:
            price_from = price_from / float(exchange.currency_rate)
            price_to = price_to / float(exchange.currency_rate)
        list_products = list_products.filter(price__range=(price_from, price_to)).all()
    elif price_from:
        if exchange:
            price_from = price_from / float(exchange.currency_rate)
        list_products = list_products.filter(price__gte=price_from).all()
    elif price_to:
        if exchange:
            price_to = price_to / float(exchange.currency_rate)
        list_products = list_products.filter(price__lte=price_to).all()

    return list_products


def engine_capacity_filter_validation(list_products, engine_capacity_from, engine_capacity_to):
    """Фильтр по объему двигателя"""
    try:
        engine_capacity_from = round(float(engine_capacity_from), 1)
    except ValueError:
        engine_capacity_from = ''

    try:
        engine_capacity_to = round(float(engine_capacity_to), 1)
    except ValueError:
        engine_capacity_to = ''

    if engine_capacity_from and engine_capacity_to:
        list_products = list_products.filter(engine_capacity__range=(engine_capacity_from, engine_capacity_to)).all()
    elif engine_capacity_from:
        list_products = list_products.filter(engine_capacity__gte=engine_capacity_from).all()
    elif engine_capacity_to:
        list_products = list_products.filter(engine_capacity__lte=engine_capacity_to).all()

    return list_products


def year_filter_validation(list_products, year_from, year_to):
    """Фильтр по году"""
    try:
        year_from = int(year_from)
    except ValueError:
        year_from = None

    try:
        year_to = int(year_to)
    except ValueError:
        year_to = None

    if year_from and year_to:
        list_products = list_products.filter(year__range=(year_from, year_to)).all()
    elif year_from:
        list_products = list_products.filter(year__gte=year_from).all()
    elif year_to:
        list_products = list_products.filter(year__lte=year_to).all()

    return list_products


def mileage_filter_validation(list_products, mileage_from, mileage_to):
    try:
        mileage_from = int(mileage_from)
    except ValueError:
        mileage_from = None

    try:
        mileage_to = int(mileage_to)
    except ValueError:
        mileage_to = None

    if mileage_from and mileage_to:
        list_products = list_products.filter(mileage__range=(mileage_from, mileage_to)).all()
    elif mileage_from:
        list_products = list_products.filter(mileage__gte=mileage_from).all()
    elif mileage_to:
        list_products = list_products.filter(mileage__lte=mileage_to).all()

    return list_products


def filter_spare_part(request, kwargs=None):
    """Фильтр Запчастей"""
    fields = get_filter_fields(request, kwargs)

    list_products = filter_brand_and_model(SparePart, fields.get('brand', ''), fields.get('model', ''))
    list_products = list_products.filter(chapter=fields.get('chapter', '')).all()

    if fields.get('category', ''):
        category = Category.objects.filter(slug=fields.get('category', '')).first()
        list_products = list_products.filter(category=category).all()

    list_products = price_filter_validation(list_products, fields.get('price_from', ''), fields.get('price_to', ''))
    return list_products.filter(in_stock=True).all()


def get_wheel_filter(request, kwargs=None):
    """Фильтр дисков"""
    fields = get_filter_fields(request, kwargs)

    list_products = filter_brand_and_model(Wheel, fields.get('brand', ''), fields.get('model', ''))

    list_products = price_filter_validation(list_products, fields.get('price_from', ''), fields.get('price_to', ''))

    try:
        diameter = round(float(fields.get('diameter', '').replace(',', '.')), 1)
    except ValueError:
        diameter = None

    if diameter:
        list_products = list_products.filter(diameter=diameter).all()

    list_products = list_products.filter(
        Q(material__icontains=fields.get('material', '')) & Q(pcd__icontains=fields.get('pcd', ''))).all()
    return list_products.filter(in_stock=True).all()


def get_tire_filter(request, kwargs=None):
    """Фильтр шин"""
    fields = get_filter_fields(request, kwargs)

    if fields.get('manufacturer', ''):
        manufacturer = Manufacturer.objects.filter(slug=fields.get('manufacturer', '')).first()
        list_products = Tire.objects.filter(manufacturer=manufacturer).all()
    else:
        list_products = Tire.objects.all()

    list_products = price_filter_validation(list_products, fields.get('price_from', ''), fields.get('price_to', ''))

    try:
        diameter = round(float(fields.get('diameter', '').replace(',', '.')), 1)
    except ValueError:
        diameter = None

    try:
        width = round(float(fields.get('width', '').replace(',', '.')), 1)
    except ValueError:
        width = None

    try:
        profile = round(float(fields.get('profile', '').replace(',', '.')), 1)
    except ValueError:
        profile = None

    if diameter:
        list_products = list_products.filter(diameter=diameter).all()

    if width:
        list_products = list_products.filter(width=width).all()

    if profile:
        list_products = list_products.filter(profile=profile).all()

    list_products = list_products.filter(
        Q(season__icontains=fields.get('season', ''))).all()
    return list_products.filter(in_stock=True).all()


def get_kit_car_filter(request, kwargs=None):
    """=++++++++++++"""
    """Фильтр машинокомплектов"""
    fields = get_filter_fields(request, kwargs)
    list_products = filter_brand_and_model(KitCar, fields.get('brand', ''), fields.get('model', ''))

    list_products = year_filter_validation(list_products, fields.get('year_from', ''), fields.get('year_to', ''))
    list_products = mileage_filter_validation(list_products, fields.get('mileage_from', ''),
                                              fields.get('mileage_to', ''))
    list_products = engine_capacity_filter_validation(list_products, fields.get('engine_capacity_from', ''),
                                                      fields.get('engine_capacity_to', ''))

    if fields.get('bodywork', ''):
        bodywork = Bodywork.objects.filter(slug=fields.get('bodywork', '')).all()
    else:
        bodywork = Bodywork.objects.all()

    if fields.get('engine_type', ''):
        engine_type = EngineType.objects.filter(slug=fields.get('engine_type', '')).all()
    else:
        engine_type = EngineType.objects.all()

    list_products = list_products.filter(
        Q(transmission__icontains=fields.get('transmission', '')) & Q(drive__icontains=fields.get('drive', '')) & Q(
            bodywork__in=bodywork) & Q(
            engine_type__in=engine_type)).all()

    list_products = price_filter_validation(list_products, fields.get('price_from', ''), fields.get('price_to', ''))

    return list_products.filter(in_stock=True).all()
