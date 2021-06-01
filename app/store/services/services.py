from ..models import Model, Brand, Category, SparePart, Cart, Wheel, KitCar, Manufacturer, Tire
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from collections import namedtuple


def get_model_class(model):
    """Модель базы данных"""
    return get_object_or_404(ContentType, model=model)


def get_model_by_id(klass, id):
    """Записись таблицы модели по ID"""
    return get_object_or_404(klass.model_class(), pk=id)


def get_cart_brand(chapter=None):
    """Вернуть марку автомобилей"""
    list_filter = namedtuple('filter', ['slug', 'title'])
    if chapter is not None:
        if chapter == 'trailer' or chapter == 'semi-trailer':
            model = get_cart_model().filter(type_model='truck').all()
            brand = {item.car_brand for item in model}
            return [list_filter(slug=item.slug, title=item.title) for item in brand]
    model = get_cart_model().filter(type_model='car').all()
    brand = {item.car_brand for item in model}
    return [list_filter(slug=item.slug, title=item.title) for item in brand]


def get_cart_brand_by_slug(slug):
    """Вернуть марку автомобилей по SLUG"""
    return Brand.objects.filter(slug=slug).first()


def get_cart_model():
    """Вернуть модель автомобилей"""
    return Model.objects.all()


def get_cart_model_by_brand_slug(car_brand_slug):
    """Вернуть модель автомобилей по SLUG марки автомобиля"""
    car_brand = get_cart_brand_by_slug(car_brand_slug)
    return Model.objects.filter(brand=car_brand)


def get_list_auto_part_for_detail(model_slug):
    car_model = get_object_or_404(Model, slug=model_slug)
    return SparePart.objects.filter(Q(model=car_model)).all()


def get_similar_auto_parts(model_slug, category_slug, product):
    car_model = get_object_or_404(Model, slug=model_slug)
    category = get_object_or_404(Category, slug=category_slug)
    return SparePart.objects.filter(Q() & Q(model=car_model) & Q(in_stock=True) & Q(category=category)).exclude(
        pk=product.pk).all()


def get_similar_kit_cat(model_slug, product):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_kit_car().filter(Q(model=car_model)).exclude(pk=product.pk).all()


def get_similar_wheel(model_slug, product):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_wheel_drive().filter(model=car_model).exclude(pk=product.pk).all()


def get_similar_tire(product):
    return get_list_tire().filter(
        Q(in_stock=True) & Q(diameter=product.diameter) & Q(width=product.width) & Q(profile=product.profile) & Q(
            season=product.season)).exclude(pk=product.pk).all()


def get_kit_car():
    """Список машинокомплектов"""
    return KitCar.objects.filter(in_stock=True).all()


def get_list_kit_car_for_detail(model_slug):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_kit_car().filter(Q(model=car_model)).all()


def get_kit_car_year():
    """Список годов машинокомплектов"""
    year = get_kit_car().values('year')
    return {item['year'] for item in year}


def get_kit_car_engine_capacity():
    """Список объемов двигателя машинокомплектов"""
    engine_capacity = get_kit_car().values('engine_capacity')
    return {item['engine_capacity'] for item in engine_capacity}


def get_wheel_drive():
    """Список дисков"""
    return Wheel.objects.filter(in_stock=True).all()


def get_list_wheel_for_detail(model_slug):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_wheel_drive().filter(model=car_model).all()


def get_wheel_drive_material():
    """Список материалов диска"""
    material = get_wheel_drive().values('material')
    return {item['material'] for item in material}


def get_wheel_drive_pcd():
    """Список PCD диска"""
    pcd = get_wheel_drive().values('pcd')
    return {item['pcd'] for item in pcd}


def get_wheel_drive_diameter():
    """Список диаметров диска"""
    diameter = get_wheel_drive().values('diameter')
    return {item['diameter'] for item in diameter}


def get_category():
    """Вернуть список категорий"""
    return Category.objects.all()


def get_wheel_drive_by_id(id):
    return get_object_or_404(Wheel, pk=id)


def get_auto_part_by_id(id):
    return get_object_or_404(SparePart, pk=id)


def get_list_tire():
    return Tire.objects.all()


def get_list_manufacturer():
    """Список производителей шин"""
    return Manufacturer.objects.all()


# def get_diameter_tire():
#     """Диаметр шин"""
#     diameter = get_list_tire().values('diameter')
#     return {item['diameter'] for item in diameter}
#
#
# def get_width_tire():
#     """Ширина шин"""
#     width = get_list_tire().values('width')
#     return {item['width'] for item in width}
#
#
# def get_profile_tire():
#     """Профиль шин"""
#     profile = get_list_tire().values('profile')
#     return {item['profile'] for item in profile}


# --------------------------------------

def get_model_class(model):
    """Модель базы данных"""
    return get_object_or_404(ContentType, model=model)


def get_brand():
    """Список марак"""
    return Brand.objects.all()


def get_brand_by_slug(slug):
    return Brand.objects.filter(slug=slug).first()


def get_brand_car():
    """Список марак авто"""
    return Brand.objects.filter(pk__in=get_model_car().values('brand')).all()


def get_brand_truck():
    """Список марак авто"""
    return Brand.objects.filter(pk__in=get_model_truck().values('brand')).all()


def get_model():
    """Список моделей"""
    return Model.objects.all()


def get_model_by_slug(slug):
    return Model.objects.filter(slug=slug).first()


def get_model_car():
    """Список моделей прицепов/полуприцепов"""
    return Model.objects.filter(type_model='car').all()


def get_model_truck():
    """Список моделей авто"""
    return Model.objects.filter(type_model='truck').all()


def get_brand_by_chapter(chapter=None):
    """Вернуть марку автомобилей"""
    if chapter is not None:
        if chapter == 'trailer' or chapter == 'semi-trailer':
            return get_brand_truck()
    return get_brand_car()


def get_model_by_chapter_brand_slug(brand_slug, chapter=None):
    """Вернуть модель по SLUG марки (Раздел)"""
    brand = get_brand_by_slug(brand_slug)
    if chapter is not None:
        if chapter == 'trailer' or chapter == 'semi-trailer':
            return get_model_truck().filter(brand=brand).all()
    return get_model_car().filter(brand=brand).all()


def get_category_car():
    return Category.objects.filter(subcategory__icontains='car').all()


def get_category_truck():
    return Category.objects.filter(subcategory__icontains='truck').all()


def get_category_by_chapter(chapter):
    """Вернуть список категорий"""
    if chapter is not None:
        if chapter == 'trailer' or chapter == 'semi-trailer':
            return get_category_truck()
    return get_category_car()


def get_kit_car_year():
    """Список годов машинокомплектов"""
    year = KitCar.objects.all().values('year').order_by('-year')
    year_uniq = {item['year'] for item in year}
    return sorted(((year, year) for year in year_uniq), key=lambda x: x[0], reverse=True)


def get_kit_car_engine_capacity():
    """Список объемов двигателя машинокомплектов"""
    engine_capacity = KitCar.objects.all().values('engine_capacity')
    engine_capacity_uniq = {item['engine_capacity'] for item in engine_capacity}
    return sorted(((engine_capacity, engine_capacity) for engine_capacity in engine_capacity_uniq), key=lambda x: x[0],
                  reverse=True)


def get_wheel_material():
    """Список материалов диска"""
    material = Wheel.objects.all().values('material')
    material_uniq = {item['material'] for item in material}
    return sorted(((material, material) for material in material_uniq), key=lambda x: x[0], reverse=True)


def get_wheel_pcd():
    """Список PCD диска"""
    pcd = Wheel.objects.all().values('pcd')
    pcd_uniq = {item['pcd'] for item in pcd}
    return sorted(((pcd, pcd) for pcd in pcd_uniq), key=lambda x: x[0], reverse=True)


def get_wheel_diameter():
    """Список диаметров диска"""
    diameter = Wheel.objects.all().values('diameter')
    diameter_uniq = {item['diameter'] for item in diameter}
    return sorted(((diameter, diameter) for diameter in diameter_uniq), key=lambda x: x[0], reverse=True)


def get_diameter_tire():
    """Диаметр шин"""
    diameter = Tire.objects.all().values('diameter')
    diameter_uniq = {item['diameter'] for item in diameter}
    return sorted(((diameter, diameter) for diameter in diameter_uniq), key=lambda x: x[0], reverse=True)


def get_width_tire():
    """Ширина шин"""
    width = Tire.objects.all().values('width')
    width_uniq = {item['width'] for item in width}
    return sorted(((width, width) for width in width_uniq), key=lambda x: x[0], reverse=True)


def get_profile_tire():
    """Профиль шин"""
    profile = Tire.objects.all().values('profile')
    profile_uniq = {item['profile'] for item in profile}
    return sorted(((profile, profile) for profile in profile_uniq), key=lambda x: x[0], reverse=True)


def get_list_manufacturer():
    """Список производителей шин"""
    return Manufacturer.objects.all()


def get_kit_car():
    return KitCar.objects.all()


def get_list_auto_part_for_detail(model_slug):
    car_model = get_object_or_404(Model, slug=model_slug)
    return SparePart.objects.filter(Q(model=car_model)).all()


def get_similar_auto_parts(model_slug, category_slug, product):
    car_model = get_object_or_404(Model, slug=model_slug)
    category = get_object_or_404(Category, slug=category_slug)
    return SparePart.objects.filter(Q() & Q(model=car_model) & Q(in_stock=True) & Q(category=category)).exclude(
        pk=product.pk).all()


def get_list_kit_car_for_detail(model_slug):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_kit_car().filter(Q(model=car_model)).all()


def get_similar_kit_cat(model_slug, product):
    car_model = get_object_or_404(Model, slug=model_slug)
    return get_kit_car().filter(Q(model=car_model)).exclude(pk=product.pk).all()
