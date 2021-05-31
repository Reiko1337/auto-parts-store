from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from .services.services import *
from .services.filter_services import *
from .services.cart_services import *
from django.contrib import messages
from .models import Tire
from django.http.response import Http404
from .models import Category
from .forms import SparePartFilter
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
    paginate_by = 1
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
        return kwargs

    def get_queryset(self):
        return get_spare_part_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('sparepart')
        return context


class DetailAutoPart(DetailView):
    """Страница товара (Автозапчасть)"""

    model = SparePart
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


class SparePartFilter(View):
    """Количестов автозапчастей (AJAX)"""

    def get(self, request, **kwargs):
        if request.is_ajax():
            products = filter_spare_part(request=self.request)
            return JsonResponse({'count': products.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class ListKitCar(ListView):
    """Страница списка машинокомплектов"""

    template_name = 'store/list-kit-car.html'
    model = KitCar
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_kit_car_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('kitcar')
        list_filter = namedtuple('filter', ['slug', 'title'])
        context['filter_fields'] = {
            'brand': get_brand_by_chapter(),
            'model': get_model_by_chapter_brand_slug(self.kwargs.get('brand')),
            'transmission': [list_filter(slug=item[0], title=item[1]) for item in KitCar.TRANSMISSION[1:]],
            'bodywork': Bodywork.objects.all(),
            'engine_type': EngineType.objects.all(),
            'drive': [list_filter(slug=item[0], title=item[1]) for item in KitCar.DRIVE[1:]],
            'year': [list_filter(slug=item, title=item) for item in get_kit_car_year()],
            'engine_capacity': [list_filter(slug=item, title=item) for item in get_kit_car_engine_capacity()]
        }
        return context


class DetailKitCar(DetailView):
    """Страница товара (Машинокомплект)"""

    model = KitCar
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
    model = Wheel
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_wheel_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_filter = namedtuple('filter', ['slug', 'title'])
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('wheel')
        context['filter_fields'] = {
            'brand': get_brand_by_chapter(),
            'model': get_model_by_chapter_brand_slug(self.kwargs.get('brand')),
            'material': [list_filter(slug=item, title=item) for item in get_wheel_drive_material()],
            'pcd': [list_filter(slug=item, title=item) for item in get_wheel_drive_pcd()],
            'diameter': [list_filter(slug=item, title=item) for item in get_wheel_drive_diameter()],
        }
        return context


class DetailWheel(DetailView):
    """Страница товара (Диск)"""

    model = Wheel
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


class ListTire(ListView):
    """Страница списка шин"""
    template_name = 'store/list-tire.html'
    model = Tire
    context_object_name = 'products'
    paginate_by = 1

    def get_queryset(self):
        return get_tire_filter(request=self.request, kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        list_filter = namedtuple('filter', ['slug', 'title'])
        context['count_products'] = self.get_queryset().count()
        context['model'] = get_model_class('tire')
        context['filter_fields'] = {
            'manufacturer': get_list_manufacturer(),
            'season': [list_filter(slug=item[0], title=item[1]) for item in Tire.SEASON[1:]],
            'diameter': [list_filter(slug=item, title=item) for item in get_diameter_tire()],
            'width': [list_filter(slug=item, title=item) for item in get_width_tire()],
            'profile': [list_filter(slug=item, title=item) for item in get_profile_tire()],
        }
        get_diameter_tire()
        return context


class DetailTire(DetailView):
    """Страница товара (Шины)"""
    model = Tire
    template_name = 'store/detail-product.html'
    context_object_name = 'product'

    def get_queryset(self):
        return get_list_tire()

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
        return render(request, 'filter/filter_select.html', context)


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


def load_categories(request):
    chapter = request.GET.get('chapter')
    if chapter:
        if chapter == 'car':
            categories = Category.objects.filter(subcategory__icontains='car').all()
        else:
            categories = Category.objects.filter(subcategory__icontains='truck').all()
    else:
        categories = Category.objects.none()
    return render(request, 'admin/model_dropdown_list_options.html', {'models': categories})


def load_brands(request):
    chapter = request.GET.get('chapter')
    list_filter = namedtuple('filter', ['pk', 'title'])
    if chapter == 'car':
        model = Model.objects.filter(type_model='car').all()
        brand = {item.brand for item in model}
        brand_list = [list_filter(pk=item.pk, title=item.title) for item in brand]
    else:
        model = Model.objects.exclude(type_model='car').all()
        brand = {item.brand for item in model}
        brand_list = [list_filter(pk=item.pk, title=item.title) for item in brand]
    return render(request, 'admin/model_dropdown_list_options.html', {'models': brand_list})


def load_models(request):
    brand_id = request.GET.get('brand')
    if brand_id:
        if request.GET.get('chapter') == 'semi-trailer' or request.GET.get('chapter') == 'trailer':
            model = Model.objects.exclude(type_model='car').order_by('title')
        else:
            model = Model.objects.filter(brand_id=brand_id, type_model='car').order_by('title')
    else:
        model = Model.objects.none()

    return render(request, 'admin/model_dropdown_list_options.html', {'models': model})
