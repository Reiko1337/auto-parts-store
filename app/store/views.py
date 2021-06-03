from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from .services.filter_services import get_brand_by_chapter, get_category_by_chapter, get_model_by_chapter_brand_slug, \
    filter_spare_part, get_model_class, get_similar_spare_parts, get_kit_car_filter, get_similar_kit_cat, \
    get_wheel_filter, get_similar_wheel, get_tire_filter, get_similar_tire, get_model_by_id
from .services.cart_services import add_item_to_cart, delete_item_to_cart
from .services.services import search_spare_part, search_wheel, search_tire, search_kit_car
from django.contrib import messages
from .models import Tire, KitCar, SparePart, Wheel
from django.http.response import Http404
from .forms import SparePartFilter, KitCarFilter, WheelFilter, TireFilter
from django.views.generic.edit import FormMixin


class AboutView(View):
    """Главная о нас"""

    template_name = 'store/about.html'

    def get(self, request):
        return render(request, self.template_name)


class ListSparePart(FormMixin, ListView):
    """Страница списка автозапчастей"""

    model = SparePart
    template_name = 'store/list-spare-part.html'
    context_object_name = 'products'
    paginate_by = 12
    form_class = SparePartFilter

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if self.kwargs.get('chapter') not in ['car', 'semi-trailer', 'trailer']:
            raise Http404

    def get_initial(self):
        initial = super().get_initial()
        initial['brand'] = self.kwargs.get('brand')
        initial['model'] = self.kwargs.get('model')
        initial['category'] = self.request.GET.get('category')
        initial['price_from'] = self.request.GET.get('price_from')
        initial['price_to'] = self.request.GET.get('price_to')
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['brand_queryset'] = get_brand_by_chapter(self.kwargs.get('chapter'))
        kwargs['category_queryset'] = get_category_by_chapter(self.kwargs.get('chapter'))

        if self.kwargs.get('brand'):
            kwargs['model_queryset'] = get_model_by_chapter_brand_slug(self.kwargs.get('brand'),
                                                                       self.kwargs.get('chapter'))
        return kwargs

    def get_queryset(self):
        return filter_spare_part(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('sparepart')
        if self.kwargs.get('chapter') == 'car':
            context['title'] = 'Автозапчасти'
        elif self.kwargs.get('chapter') == 'trailer':
            context['title'] = 'Запчасти на прицеп'
        elif self.kwargs.get('chapter') == 'semi-trailer':
            context['title'] = 'Запчасти на полуприцеп'
        context['url_ajax'] = '/list/spare-part/{0}/'.format(self.kwargs.get('chapter'))
        return context


class DetailSparePart(DetailView):
    """Страница товара (Автозапчасть)"""

    model = SparePart
    template_name = 'store/detail-product.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        context['similar_products'] = get_similar_spare_parts(self.kwargs.get('model'), self.kwargs.get('category'),
                                                              product)
        return context


class SparePartFilter(View):
    """Количестов автозапчастей (AJAX)"""

    def get(self, request, **kwargs):
        if request.is_ajax():
            products = filter_spare_part(request=self.request)
            return JsonResponse({'count': products.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class ListKitCar(FormMixin, ListView):
    """Страница списка машинокомплектов"""

    template_name = 'store/list-kit-car.html'
    model = KitCar
    context_object_name = 'products'
    paginate_by = 12
    form_class = KitCarFilter

    def get_initial(self):
        initial = super().get_initial()
        initial['brand'] = self.kwargs.get('brand')
        initial['model'] = self.kwargs.get('model')
        initial['year_from'] = self.request.GET.get('year_from')
        initial['year_to'] = self.request.GET.get('year_to')
        initial['mileage_from'] = self.request.GET.get('mileage_from')
        initial['mileage_to'] = self.request.GET.get('mileage_to')
        initial['transmission'] = self.request.GET.get('transmission')
        initial['bodywork'] = self.request.GET.get('bodywork')
        initial['engine_type'] = self.request.GET.get('engine_type')
        initial['drive'] = self.request.GET.get('drive')
        initial['engine_capacity_from'] = self.request.GET.get('engine_capacity_from')
        initial['engine_capacity_to'] = self.request.GET.get('engine_capacity_to')
        initial['price_from'] = self.request.GET.get('price_from')
        initial['price_to'] = self.request.GET.get('price_to')
        return initial

    def get_queryset(self):
        return get_kit_car_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('kitcar')
        context['url_ajax'] = '/list/kit-car/'
        return context


class DetailKitCar(DetailView):
    """Страница товара (Машинокомплект)"""

    model = KitCar
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

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


class ListWheel(FormMixin, ListView):
    """Страница списка дисков"""

    template_name = 'store/list-wheel.html'
    model = Wheel
    context_object_name = 'products'
    paginate_by = 12
    form_class = WheelFilter

    def get_initial(self):
        initial = super().get_initial()
        initial['brand'] = self.kwargs.get('brand')
        initial['model'] = self.kwargs.get('model')
        initial['material'] = self.request.GET.get('material')
        initial['diameter'] = self.request.GET.get('diameter')
        initial['pcd'] = self.request.GET.get('pcd')
        initial['price_from'] = self.request.GET.get('price_from')
        initial['price_to'] = self.request.GET.get('price_to')
        return initial

    def get_queryset(self):
        return get_wheel_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('wheel')
        context['url_ajax'] = '/list/wheel/'
        return context


class DetailWheel(DetailView):
    """Страница товара (Диск)"""

    model = Wheel
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

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


class ListTire(FormMixin, ListView):
    """Страница списка шин"""
    template_name = 'store/list-tire.html'
    model = Tire
    context_object_name = 'products'
    paginate_by = 12
    form_class = TireFilter

    def get_initial(self):
        initial = super().get_initial()
        initial['manufacturer'] = self.request.GET.get('manufacturer')
        initial['season'] = self.request.GET.get('season')
        initial['diameter'] = self.request.GET.get('diameter')
        initial['width'] = self.request.GET.get('width')
        initial['profile'] = self.request.GET.get('profile')
        initial['price_from'] = self.request.GET.get('price_from')
        initial['price_to'] = self.request.GET.get('price_to')
        return initial

    def get_queryset(self):
        return get_tire_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('tire')
        context['url_ajax'] = '/list/tire/'
        return context


class DetailTire(DetailView):
    """Страница товара (Шины)"""
    model = Tire
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = super().get_object()
        context['similar_products'] = get_similar_tire(product)
        return context


class TireFilter(View):
    """Количестов шин (AJAX)"""

    def get(self, request):
        if request.is_ajax():
            tire = get_tire_filter(request=self.request)
            return JsonResponse({'count': tire.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class FilterModelsGenerate(View):
    """Список моделей автомобилей (AJAX)"""

    def get(self, request):
        brand = request.GET.get('brand')
        chapter = request.GET.get('chapter')
        context = {
            'items': get_model_by_chapter_brand_slug(brand, chapter)
        }
        return render(request, 'filter/filter_select_option.html', context)


class SearchResultView(View):
    """Результат поиска"""
    template_name = 'store/list-search(favorite).html'

    def get(self, request):
        q = request.GET.get('q', '')
        if q:
            context = {
                'q': q,
                'title': 'Результат поиска',
                'spare_part': {
                    'list': search_spare_part(q),
                    'model': get_model_class('sparepart')
                },
                'kit_car': {
                    'list': search_kit_car(q),
                    'model': get_model_class('kitcar')
                },
                'wheel': {
                    'list': search_wheel(q),
                    'model': get_model_class('wheel')
                },
                'tire': {
                    'list': search_tire(q),
                    'model': get_model_class('tire')
                }
            }
        else:
            context = {'title': 'Результат поиска'}
        return render(request, self.template_name, context)


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
