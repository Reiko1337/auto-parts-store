from ..models import Model, Brand, Category, SparePart, Wheel, KitCar, Tire
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


def get_model_by_id(klass, id):
    """Записись таблицы модели по ID"""
    return get_object_or_404(klass.model_class(), pk=id)


def get_wheel():
    """Список дисков"""
    return Wheel.objects.filter(in_stock=True).all()


def get_model_class(model):
    """Модель базы данных"""
    return get_object_or_404(ContentType, model=model)


def get_brand_by_slug(slug):
    """Марка по SLUG"""
    return Brand.objects.filter(slug=slug).first()


def get_brand_by_id(id):
    """Марка по ID"""
    return Brand.objects.filter(pk=id).first()


def get_brand_car():
    """Список марак авто"""
    return Brand.objects.filter(pk__in=get_model_car().values('brand')).all()


def get_brand_truck():
    """Список марак авто"""
    return Brand.objects.filter(pk__in=get_model_truck().values('brand')).all()


def get_model_none():
    return Model.objects.none()


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


def get_model_by_chapter_brand_id(brand_id, chapter=None):
    """Вернуть модель по SLUG марки (Раздел)"""
    brand = get_brand_by_id(brand_id)
    if chapter is not None:
        if chapter == 'trailer' or chapter == 'semi-trailer':
            return get_model_truck().filter(brand=brand).all()
    return get_model_car().filter(brand=brand).all()


def get_category_none():
    return Category.objects.none()


def get_category_car():
    """Категория автомобилей"""
    return Category.objects.filter(subcategory__icontains='car').all()


def get_category_truck():
    """категория прицепов"""
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


def get_similar_spare_parts(model_slug, category_slug, product):
    """Похожие запчасти"""
    model = get_object_or_404(Model, slug=model_slug)
    category = get_object_or_404(Category, slug=category_slug)
    return SparePart.objects.filter(Q() & Q(model=model) & Q(in_stock=True) & Q(category=category)).exclude(
        pk=product.pk).all()


def get_similar_kit_cat(model_slug, product):
    """Похожие машинокомлекты"""
    car_model = get_object_or_404(Model, slug=model_slug)
    return KitCar.objects.filter(Q(model=car_model)).exclude(pk=product.pk).all()


def get_similar_wheel(model_slug, product):
    """Похожие диски"""
    model = get_object_or_404(Model, slug=model_slug)
    return get_wheel().filter(model=model).exclude(pk=product.pk).all()


def get_similar_tire(product):
    """Похожие шины"""
    return Tire.objects.filter(
        Q(in_stock=True) & Q(diameter=product.diameter) & Q(width=product.width) & Q(profile=product.profile) & Q(
            season=product.season)).exclude(pk=product.pk).all()


def search_spare_part(q):
    """Поиск запчасти"""
    return SparePart.objects.filter(Q(in_stock=True) & Q(article__icontains=q))


def search_wheel(q):
    """Поиск дисков"""
    return Wheel.objects.filter(Q(in_stock=True) & Q(article__icontains=q))


def search_tire(q):
    """Поиск шин"""
    return Tire.objects.filter(Q(in_stock=True) & Q(article__icontains=q))


def search_kit_car(q):
    """Поиск машинокомплекта"""
    return KitCar.objects.filter(Q(in_stock=True) & Q(vin__icontains=q))
