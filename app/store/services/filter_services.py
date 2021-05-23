from ..models import CarModel, CarBrand, Category, AutoPart, Cart, WheelDrive, Car, Bodywork, EngineType
from django.db.models import Q


def get_filter_fields(item_model, request, kwargs=None):
    """Поля фильтрации"""
    if kwargs is not None:
        brand = kwargs.get('brand')
        model = kwargs.get('model')
    else:
        brand = request.GET.get('brand')
        model = request.GET.get('model')

    price_from = request.GET.get('priceFrom') if request.GET.get('priceFrom') else ''
    price_to = request.GET.get('priceTo') if request.GET.get('priceTo') else ''

    fields = {
        'brand': brand,
        'model': model,
        'price_from': price_from.replace(',', '.'),
        'price_to': price_to.replace(',', '.')
    }

    if item_model is AutoPart:
        fields['spare_part'] = request.GET.get('part')

    if item_model is Car:
        fields['transmission'] = request.GET.get('transmission') if request.GET.get('transmission') else ''
        fields['bodywork'] = request.GET.get('bodywork')
        fields['engine_type'] = request.GET.get('engineType')
        fields['drive'] = request.GET.get('drive') if request.GET.get('drive') else ''
        fields['mileage_from'] = request.GET.get('mileageFrom') if request.GET.get('mileageFrom') else ''
        fields['mileage_to'] = request.GET.get('mileageTo') if request.GET.get('mileageTo') else ''
        fields['year_from'] = request.GET.get('yearFrom') if request.GET.get('yearFrom') else ''
        fields['year_to'] = request.GET.get('yearTo') if request.GET.get('yearTo') else ''
        fields['engine_capacity_from'] = request.GET.get('engineCapacityFrom').replace(',', '.') if request.GET.get(
            'engineCapacityFrom') else ''
        fields['engine_capacity_to'] = request.GET.get('engineCapacityTo').replace(',', '.') if request.GET.get(
            'engineCapacityTo') else ''

    if item_model is WheelDrive:
        fields['diameter'] = request.GET.get('diameter') if request.GET.get('diameter') else ''
        fields['material'] = request.GET.get('material') if request.GET.get('material') else ''
        fields['pcd'] = request.GET.get('pcd') if request.GET.get('pcd') else ''

    return fields


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

    if price_from and price_to:
        list_products = list_products.filter(price__range=(price_from, price_to)).all()
    elif price_from:
        list_products = list_products.filter(price__gte=price_from).all()
    elif price_to:
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
    """Фильтр по пробегу"""
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


def filter_brand_and_model(model, brand_slug, model_slug):
    """Фильтр по марке и модели автомобиля"""
    if brand_slug:
        car_brand = CarBrand.objects.filter(slug=brand_slug).first()
        if model_slug:
            if model_slug:
                car_model = CarModel.objects.filter(slug=model_slug).all()
            else:
                car_model = CarModel.objects.filter(car_brand=car_brand).all()
            list_products = model.objects.filter(car_model__in=car_model).all()
        else:
            car_model = CarModel.objects.filter(car_brand=car_brand).all()
            list_products = model.objects.filter(car_model__in=car_model).all()
    else:
        list_products = model.objects.all()

    return list_products


def get_car_models_filter(brand):
    """Вернуть список моделей автомобилей (AJAX)"""
    brand_slug = brand
    car_brand_first = CarBrand.objects.filter(slug=brand_slug).first()
    queryset = CarModel.objects.filter(car_brand=car_brand_first).all().values('title', 'slug')
    return queryset


def get_auto_part_filter(request, kwargs=None):
    """Фильтр автозапчастей"""

    fields = get_filter_fields(AutoPart, request, kwargs)

    list_products = filter_brand_and_model(AutoPart, fields['brand'], fields['model'])

    if fields['spare_part']:
        category = Category.objects.filter(slug=fields['spare_part']).first()
        list_products = list_products.filter(category=category).all()

    list_products = price_filter_validation(list_products, fields['price_from'], fields['price_to'])

    return list_products.filter(in_stock=True).all()


def get_wheel_filter(request, kwargs=None):
    """Фильтр дисков"""
    fields = get_filter_fields(WheelDrive, request, kwargs)

    list_products = filter_brand_and_model(WheelDrive, fields['brand'], fields['model'])

    list_products = price_filter_validation(list_products, fields['price_from'], fields['price_to'])

    try:
        diameter = int(fields['diameter'])
    except ValueError:
        diameter = None

    if diameter:
        list_products = list_products.filter(diameter=diameter).all()

    list_products = list_products.filter(
        Q(material__icontains=fields['material']) & Q(pcd__icontains=fields['pcd'])).all()
    return list_products.filter(in_stock=True).all()


def get_kit_car_filter(request, kwargs=None):
    """Фильтр машинокомплектов"""
    fields = get_filter_fields(Car, request, kwargs)

    list_products = filter_brand_and_model(Car, fields['brand'], fields['model'])

    list_products = year_filter_validation(list_products, fields['year_from'], fields['year_to'])
    list_products = mileage_filter_validation(list_products, fields['mileage_from'], fields['mileage_to'])
    list_products = engine_capacity_filter_validation(list_products, fields['engine_capacity_from'],
                                                      fields['engine_capacity_to'])

    if fields['bodywork']:
        bodywork = Bodywork.objects.filter(slug=fields['bodywork']).all()
    else:
        bodywork = Bodywork.objects.all()

    if fields['engine_type']:
        engine_type = EngineType.objects.filter(slug=fields['engine_type']).all()
    else:
        engine_type = EngineType.objects.all()

    list_products = list_products.filter(
        Q(transmission__icontains=fields['transmission']) & Q(drive__icontains=fields['drive']) & Q(
            bodywork__in=bodywork) & Q(
            engine_type__in=engine_type)).all()

    list_products = price_filter_validation(list_products, fields['price_from'], fields['price_to'])

    return list_products.filter(in_stock=True).all()
