from django import template
from ..models import KitCar, SparePart, Wheel, Tire
from customer.services.favorite_services import product_is_favorite

register = template.Library()


@register.inclusion_tag('store/tags/tag-list-product.html')
def tag_list_product(model, items):
    model = model.model_class()
    count_column = 2
    products = []
    if model is SparePart:
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.get_price(),
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_brand__title(),
                    'Модель': item.get_model__title(),
                    'Артикул': item.article,
                }
            }
            products.append(info)
    elif model is KitCar:
        count_column = 1
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.get_price(),
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_brand__title(),
                    'Модель': item.get_model__title(),
                    'Год': item.year,
                    'Пробег': item.mileage,
                    'Кузов': item.bodywork.title,
                    'Тип двигателя': item.engine_type,
                    'Объем двигателя': str(item.engine_capacity) + ' л',
                    'Коробка передач': item.get_transmission_display(),
                    'Привод': item.get_drive_display(),
                    'Цвет': item.color
                }
            }
            products.append(info)
    elif model is Wheel:
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.get_price(),
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_brand__title(),
                    'Модель': item.get_model__title(),
                    'Артикул': item.article,
                    'Материал': item.material,
                    'Диаметр': f'R {item.diameter}',
                    'Сверловка (PCD)': item.pcd
                }
            }
            products.append(info)
    elif model is Tire:
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.get_price(),
                'url': item.get_absolute_url(),
                'specification': {
                    'Производитель': item.get_manufacturer(),
                    'Сезон': item.get_season_display(),
                    'Диаметр': f'R {item.diameter}',
                    'Ширина': item.width,
                    'Профиль': item.profile
                }
            }
            products.append(info)

    return {'products': products, 'count_column': count_column}


@register.inclusion_tag('store/tags/tag-detail-product.html')
def tag_detail_product(product, similar_product, user):
    model = product.get_model_name()
    if model == 'sparepart':
        info = {
            'id': product.id,
            'in_stock': product.in_stock,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.get_price(),
            'specification': {
                'Марка': product.get_brand__title(),
                'Модель': product.get_model__title(),
                'Категория': product.get_category__title,
                'Артикул': product.article,
            },
            'description': product.description,
            'additional_images': product.additional_photo.all(),
            'is_favorite': product_is_favorite(product, user)
        }
    elif model == 'kitcar':
        info = {
            'id': product.id,
            'in_stock': product.in_stock,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.get_price(),
            'specification': {
                'Марка': product.get_brand__title(),
                'Модель': product.get_model__title(),
                'VIN': product.vin,
                'Год': product.year,
                'Пробег': product.mileage,
                'Кузов': product.bodywork.title,
                'Тип двигателя': product.engine_type,
                'Объем двигателя': str(product.engine_capacity) + ' л',
                'Коробка передач': product.get_transmission_display(),
                'Привод': product.get_drive_display(),
                'Цвет': product.color
            },
            'description': product.description,
            'additional_images': product.additional_photo.all(),
            'is_favorite': product_is_favorite(product, user)
        }
    elif model == 'wheel':
        info = {
            'id': product.id,
            'in_stock': product.in_stock,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.get_price(),
            'specification': {
                'Марка': product.get_brand__title(),
                'Модель': product.get_model__title(),
                'Артикул': product.article,
                'Материал': product.material,
                'Диаметр': f'R {product.diameter}',
                'Сверловка (PCD)': product.pcd
            },
            'description': product.description,
            'additional_images': product.additional_photo.all(),
            'is_favorite': product_is_favorite(product, user)
        }
    elif model == 'tire':
        info = {
            'id': product.id,
            'in_stock': product.in_stock,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.get_price(),
            'specification': {
                'Производитель': product.get_manufacturer(),
                'Сезон': product.get_season_display(),
                'Диаметр': f'R {product.diameter}',
                'Ширина': product.width,
                'Профиль': product.profile
            },
            'description': product.description,
            'additional_images': product.additional_photo.all(),
            'is_favorite': product_is_favorite(product, user)
        }
    return {'product': info, 'similar_product': similar_product}


@register.inclusion_tag('store/tags/tag-media-product.html')
def tag_media(product):
    model_db = product.get_model_name()
    context = {
        'meta_description': '',
        'meta_keywords': ''
    }
    if model_db == 'kitcar':
        context['meta_description'] += f'{product.meta_description} '
        context['meta_description'] += f'{product.model.meta_description} '
        context['meta_description'] += f'{product.model.brand.meta_description} '
        context['meta_description'] += f'{product.bodywork.meta_description} '
        context['meta_description'] += f'{product.engine_type.meta_description} '

        context['meta_keywords'] += f'{product.meta_keywords} '
        context['meta_keywords'] += f'{product.model.meta_keywords} '
        context['meta_keywords'] += f'{product.model.brand.meta_keywords} '
        context['meta_keywords'] += f'{product.bodywork.meta_keywords} '
        context['meta_keywords'] += f'{product.engine_type.meta_keywords} '
    elif model_db == 'sparepart':
        context['meta_description'] += f'{product.meta_description} '
        context['meta_description'] += f'{product.model.meta_description} '
        context['meta_description'] += f'{product.model.brand.meta_description} '
        context['meta_description'] += f'{product.category.meta_description} '

        context['meta_keywords'] += f'{product.meta_keywords} '
        context['meta_keywords'] += f'{product.model.meta_keywords} '
        context['meta_keywords'] += f'{product.model.brand.meta_keywords} '
        context['meta_keywords'] += f'{product.category.meta_keywords} '
    elif model_db == 'wheel':
        context['meta_description'] += f'{product.meta_description} '
        context['meta_description'] += f'{product.model.meta_description} '
        context['meta_description'] += f'{product.model.brand.meta_description} '

        context['meta_keywords'] += f'{product.meta_keywords} '
        context['meta_keywords'] += f'{product.model.meta_keywords} '
        context['meta_keywords'] += f'{product.model.brand.meta_keywords} '
    elif model_db == 'tire':
        context['meta_description'] += f'{product.meta_description} '
        context['meta_description'] += f'{product.manufacturer.meta_description} '
        context['meta_keywords'] += f'{product.meta_keywords} '
        context['meta_keywords'] += f'{product.manufacturer.meta_keywords} '

    return context
