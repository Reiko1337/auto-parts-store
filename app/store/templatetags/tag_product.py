from django import template
from ..models import Car, AutoPart, WheelDrive

register = template.Library()


@register.inclusion_tag('store/tags/tag-list-product.html')
def tag_list_product(model, items):
    model = model.model_class()
    count_column = 2
    products = []
    if model is AutoPart:
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.price,
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_car_brand__title(),
                    'Модель': item.get_car_model__title(),
                    'Артикул': item.article,
                }
            }
            products.append(info)
    elif model is Car:
        count_column = 1
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.price,
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_car_brand__title(),
                    'Модель': item.get_car_model__title(),
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
    elif model is WheelDrive:
        for item in items:
            info = {
                'id': item.id,
                'model_name': item.get_model_name,
                'title': item.get_title(),
                'image': item.image.url,
                'price': item.price,
                'url': item.get_absolute_url(),
                'specification': {
                    'Марка': item.get_car_brand__title(),
                    'Модель': item.get_car_model__title(),
                    'Артикул': item.article,
                    'Материал': item.material,
                    'Диаметр': f'R {item.diameter}',
                    'Сверловка (PCD)': item.pcd
                }
            }
            products.append(info)

    return {'products': products, 'count_column': count_column}


@register.inclusion_tag('store/tags/tag-detail-product.html')
def tag_detail_product(product, similar_product):
    model = product.get_model_name()
    if model == 'autopart':
        info = {
            'id': product.id,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.price,
            'specification': {
                'Марка': product.get_car_brand__title(),
                'Модель': product.get_car_model__title(),
                'Категория': product.get_category__title,
                'Артикул': product.article,
            },
            'description': product.description,
            'additional_images': product.additional_photo.all()
        }
    elif model == 'car':
        info = {
            'id': product.id,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.price,
            'specification': {
                'Марка': product.get_car_brand__title(),
                'Модель': product.get_car_model__title(),
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
            'additional_images': product.additional_photo.all()
        }
    elif model == 'wheeldrive':
        info = {
            'id': product.id,
            'model_name': product.get_model_name,
            'title': product.get_title(),
            'image': product.image.url,
            'price': product.price,
            'specification': {
                'Марка': product.get_car_brand__title(),
                'Модель': product.get_car_model__title(),
                'Артикул': product.article,
                'Материал': product.material,
                'Диаметр': f'R {product.diameter}',
                'Сверловка (PCD)': product.pcd
            },
            'description': product.description,
            'additional_images': product.additional_photo.all()
        }
    return {'product': info, 'similar_product': similar_product}
