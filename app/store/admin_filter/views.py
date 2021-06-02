from django.shortcuts import render
from ..services.services import get_category_by_chapter, get_category_none, get_brand_by_chapter, \
    get_model_by_chapter_brand_id, get_model_none


def load_categories(request):
    """Ajax запрос (Категория)"""
    chapter = request.GET.get('chapter')
    if chapter:
        categories = get_category_by_chapter(chapter)
    else:
        categories = get_category_none()
    return render(request, 'admin/dropdown_list_options.html', {'items': categories})


def load_brands(request):
    """Ajax запрос (Марка)"""
    chapter = request.GET.get('chapter')
    brand_list = get_brand_by_chapter(chapter)
    return render(request, 'admin/dropdown_list_options.html', {'items': brand_list})


def load_models(request):
    """Ajax запрос (Модель)"""
    brand_id = request.GET.get('brand')
    if brand_id:
        model = get_model_by_chapter_brand_id(brand_id, request.GET.get('chapter'))
    else:
        model = get_model_none()

    return render(request, 'admin/dropdown_list_options.html', {'items': model})
