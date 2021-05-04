from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import View, ListView, DetailView, CreateView
from django.contrib.auth.views import LoginView
from .models import AutoPart, CarModel, CartContent, WheelDrive, Car, Bodywork, EngineType
from .services import get_cart_model, get_category, get_cart_brand, get_auto_parts_filter, get_car_models_filter, \
    get_cart_model_by_brand_slug, get_cart_auth_user, add_item_to_cart, delete_item_to_cart, get_wheel_drive_by_id, \
    get_auto_part_by_id, get_model_class, get_model_by_id, get_cart_brand_by_slug, get_wheel_drive_filter, \
    get_kid_car_filter
from .session import CartSession
from .forms import AutoPartFilter
from collections import namedtuple
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class Main(View):
    """Главная страница"""
    template_name = 'store/main.html'

    def get(self, request):
        return render(request, self.template_name)


class ListAutoParts(ListView):
    """Страница список запчастей"""
    template_name = 'store/auto_parts.html'
    model = AutoPart
    context_object_name = 'parts'

    def get_queryset(self):
        brand_slug = self.kwargs.get('brand') if self.kwargs.get('brand') else ''
        model_slug = self.kwargs.get('model') if self.kwargs.get('model') else ''
        part_slug = self.request.GET.get('part') if self.request.GET.get('part') else ''
        return get_auto_parts_filter(brand_slug, model_slug, part_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_brands'] = get_cart_brand()
        context['car_models'] = get_cart_model_by_brand_slug(self.kwargs.get('brand'))
        context['categories'] = get_category()
        return context


class ListWheelsDrive(ListView):
    """Страница список дисков"""
    template_name = 'store/wheel_drive.html'
    model = WheelDrive
    context_object_name = 'wheels'

    def get_queryset(self):
        brand_slug = self.kwargs.get('brand') if self.kwargs.get('brand') else ''
        model_slug = self.kwargs.get('model') if self.kwargs.get('model') else ''
        diameter = self.request.GET.get('diameter') if self.request.GET.get('diameter') else ''
        material = self.request.GET.get('material') if self.request.GET.get('material') else ''
        pcd = self.request.GET.get('pcd') if self.request.GET.get('pcd') else ''
        return get_wheel_drive_filter(brand_slug, model_slug, diameter, material, pcd)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_brands'] = get_cart_brand()
        context['car_models'] = get_cart_model_by_brand_slug(self.kwargs.get('brand'))
        wheel_drive = WheelDrive.objects.all()
        context['wheels_filter_material'] = wheel_drive.order_by('material').distinct('material')
        context['wheels_filter_pcd'] = wheel_drive.order_by('pcd').distinct('pcd')
        context['wheels_filter_diameter'] = wheel_drive.order_by('diameter').distinct('diameter')
        return context


class ListKidsCar(ListView):
    """Страница список машинокомплектов"""
    template_name = 'store/cars.html'
    model = Car
    context_object_name = 'cars'

    def get_queryset(self):
        brand_slug = self.kwargs.get('brand') if self.kwargs.get('brand') else ''
        model_slug = self.kwargs.get('model') if self.kwargs.get('model') else ''
        transmission = self.request.GET.get('transmission') if self.request.GET.get('transmission') else ''
        bodywork = self.request.GET.get('bodywork') if self.request.GET.get('bodywork') else ''
        engine_type = self.request.GET.get('engine_type') if self.request.GET.get('engine_type') else ''
        drive = self.request.GET.get('drive') if self.request.GET.get('drive') else ''
        return get_kid_car_filter(brand_slug, model_slug, transmission, bodywork, engine_type, drive)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_brands'] = get_cart_brand()
        context['car_models'] = get_cart_model_by_brand_slug(self.kwargs.get('brand'))
        car_filter = namedtuple('filter', ['slug', 'title'])
        context['car_transmission'] = [car_filter(slug=item[0], title=item[1]) for item in Car.TRANSMISSION[1:]]
        context['car_bodywork'] = Bodywork.objects.all()
        context['car_engine_type'] = EngineType.objects.all()
        context['car_drive'] = [car_filter(slug=item[0], title=item[1]) for item in Car.DRIVE[1:]]
        return context


class DetailAutoPart(DetailView):
    model = AutoPart
    template_name = 'store/detail_auto_parts.html'
    context_object_name = 'part'
    slug_url_kwarg = 'auto_part'

    def get_queryset(self):
        car_model = get_object_or_404(CarModel, slug=self.kwargs.get('model'))
        return AutoPart.objects.filter(car_model=car_model).all()


class DetailWheelDrive(DetailView):
    model = WheelDrive
    template_name = 'store/detail_wheels_drive.html'
    context_object_name = 'wheel'
    slug_url_kwarg = 'wheel_drive'

    def get_queryset(self):
        car_model = get_object_or_404(CarModel, slug=self.kwargs.get('model'))
        return WheelDrive.objects.filter(car_model=car_model).all()


class DetailKidCar(DetailView):
    model = WheelDrive
    template_name = 'store/detail_kids_car.html'
    context_object_name = 'car'
    slug_url_kwarg = 'car'

    def get_queryset(self):
        car_model = get_object_or_404(CarModel, slug=self.kwargs.get('model'))
        return Car.objects.filter(car_model=car_model).all()


class FilterModelsGenerate(View):
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
            add_item_to_cart(request, item)
        return redirect(request.META['HTTP_REFERER'])


class DeleteItemInCart(View):
    """Удалить из корзины"""

    def get(self, request, model, id):
        delete_item_to_cart(request, model, id)
        return redirect(request.META['HTTP_REFERER'])


class TestView(View):
    def get(self, request):
        print(request.GET)
        f = AutoPartFilter(request.GET)
        return render(request, 'store/test.html', {'filter': f})


class WheelDriveFilter(View):
    def get(self, request):
        if request.is_ajax():
            brand_slug = request.GET.get('brand')
            model_slug = request.GET.get('model')
            diameter = request.GET.get('diameter')
            material = request.GET.get('material')
            pcd = request.GET.get('pcd')
            wheel_drive = get_wheel_drive_filter(brand_slug, model_slug, diameter, material, pcd)
            return JsonResponse({'count': wheel_drive.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class AutoPartFilter(View):
    def get(self, request):
        if request.is_ajax():
            brand_slug = request.GET.get('brand')
            model_slug = request.GET.get('model')
            part_slug = request.GET.get('part')
            auto_part = get_auto_parts_filter(brand_slug, model_slug, part_slug)
            return JsonResponse({'count': auto_part.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class KidCarFilter(View):
    def get(self, request):
        if request.is_ajax():
            brand_slug = request.GET.get('brand')
            model_slug = request.GET.get('model')
            transmission = request.GET.get('transmission')
            bodywork = request.GET.get('bodywork')
            engine_type = request.GET.get('engineType')
            drive = request.GET.get('drive')
            kid_car = get_kid_car_filter(brand_slug, model_slug, transmission, bodywork, engine_type, drive)
            return JsonResponse({'count': kid_car.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)
