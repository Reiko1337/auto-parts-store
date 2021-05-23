from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from collections import namedtuple
from .services.services import *
from .services.filter_services import *
from .services.cart_services import *
from django.contrib import messages


class AboutView(View):
    """Главная о нас"""
    template_name = 'store/about.html'

    def get(self, request):
        return render(request, self.template_name)


class ListAutoPart(ListView):
    """Страница списка автозапчастей"""

    model = AutoPart
    template_name = 'store/list-auto-part.html'
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_auto_part_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('autopart')
        context['filter_fields'] = {
            'brand': get_cart_brand(),
            'model': get_cart_model_by_brand_slug(self.kwargs.get('brand')),
            'category': get_category()
        }
        return context


class DetailAutoPart(DetailView):
    """Страница товара (Автозапчасть)"""
    model = AutoPart
    template_name = 'store/detail-product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return get_list_auto_part_for_detail(self.kwargs.get('model'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        context['similar_products'] = get_similar_auto_parts(self.kwargs.get('model'), self.kwargs.get('category'),
                                                             product)
        return context


class AutoPartFilter(View):
    """Количестов автозапчастей (AJAX)"""

    def get(self, request):
        if request.is_ajax():
            auto_part = get_auto_part_filter(request=self.request)
            return JsonResponse({'count': auto_part.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class ListKitCar(ListView):
    """Страница списка машинокомплектов"""

    template_name = 'store/list-kit-car.html'
    model = Car
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_kit_car_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('car')
        list_filter = namedtuple('filter', ['slug', 'title'])
        context['filter_fields'] = {
            'brand': get_cart_brand(),
            'model': get_cart_model_by_brand_slug(self.kwargs.get('brand')),
            'transmission': [list_filter(slug=item[0], title=item[1]) for item in Car.TRANSMISSION[1:]],
            'bodywork': Bodywork.objects.all(),
            'engine_type': EngineType.objects.all(),
            'drive': [list_filter(slug=item[0], title=item[1]) for item in Car.DRIVE[1:]],
            'year': get_kit_car_year(),
            'engine_capacity': get_kit_car_engine_capacity()
        }
        return context


class DetailKitCar(DetailView):
    """Страница товара (Машинокомплект)"""
    model = WheelDrive
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

    def get_queryset(self):
        return get_list_kit_car_for_detail(self.kwargs.get('model'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        context['similar_products'] = get_similar_kit_cat(self.kwargs.get('model'), product)
        return context


class KitCarFilter(View):
    """Количестов машинокомплектов (AJAX)"""

    def get(self, request):
        if request.is_ajax():
            kid_car = get_kit_car_filter(request=self.request)
            return JsonResponse({'count': kid_car.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class ListWheel(ListView):
    """Страница списка дисков"""
    template_name = 'store/list-wheel-drive.html'
    model = WheelDrive
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_wheel_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('wheeldrive')
        context['filter_fields'] = {
            'brand': get_cart_brand(),
            'model': get_cart_model_by_brand_slug(self.kwargs.get('brand')),
            'material': get_wheel_drive_material(),
            'pcd': get_wheel_drive_pcd(),
            'diameter': get_wheel_drive_diameter()
        }
        return context


class DetailWheel(DetailView):
    """Страница товара (Диск)"""
    model = WheelDrive
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

    def get_queryset(self):
        return get_list_wheel_for_detail(self.kwargs.get('model'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        context['similar_products'] = get_similar_wheel(self.kwargs.get('model'), product)
        return context


class WheelFilter(View):
    """Количестов дисков (AJAX)"""

    def get(self, request):
        if request.is_ajax():
            wheel_drive = get_wheel_filter(request=self.request)
            return JsonResponse({'count': wheel_drive.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class FilterModelsGenerate(View):
    """Список моделей автомобилей (AJAX)"""

    def get(self, request):
        if request.is_ajax():
            queryset = get_car_models_filter(request.GET.get('brand'))
            return JsonResponse({'models': list(queryset)}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class AddToCart(View):
    """Добавить в корзину"""

    def get(self, request, model, id):
        content_type = get_model_class(model)
        item = get_model_by_id(content_type, id)
        if item.in_stock:
            result = add_item_to_cart(request, item)
            if result:
                messages.success(request, 'Товар добавлен в корзину')
            else:
                messages.info(request, 'Товар уже в корзине')
        else:
            messages.error(request, 'Товара нет в наличии')
        return redirect(request.META['HTTP_REFERER'])


class DeleteItemInCart(View):
    """Удалить из корзины"""

    def get(self, request, model, id):
        delete_item_to_cart(request, model, id)
        messages.info(request, 'Товар был удален из корзины')
        return redirect(request.META['HTTP_REFERER'])
