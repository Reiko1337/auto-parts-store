from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.views import LoginView
from .models import AutoPart, CarModel, CartContent
from .services import get_cart_model, get_category, get_cart_brand, get_auto_parts_filter, get_car_models_filter, \
    get_cart_model_by_brand_slug, get_cart_auth_user, add_item_to_cart, delete_item_to_cart
from .session import CartSession
from .services_auth_user import CartUser


class Main(View):
    template_name = 'store/main.html'

    def get(self, request):
        return render(request, self.template_name)


class ListAutoParts(ListView):
    template_name = 'store/auto_parts.html'
    model = AutoPart
    context_object_name = 'parts'

    def get_queryset(self):
        return get_auto_parts_filter(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['car_brands'] = get_cart_brand()
        context['car_models'] = get_cart_model_by_brand_slug(self.request.GET.get('brand'))
        context['categories'] = get_category()
        return context


class DetailAutoPart(DetailView):
    model = AutoPart
    template_name = 'store/detail_auto_parts.html'
    context_object_name = 'part'
    slug_url_kwarg = 'auto_part'

    def get_queryset(self):
        car_model = get_object_or_404(CarModel, slug=self.kwargs.get('model'))
        return AutoPart.objects.filter(car_model=car_model).all()


class FilterModelsGenerate(View):
    def get(self, request):
        if request.is_ajax():
            auto_part = get_auto_parts_filter(request)
            queryset = get_car_models_filter(request)
            return JsonResponse({'models': list(queryset), 'count': auto_part.count()}, status=200, safe=False)
        return JsonResponse({'success': False}, status=404)


class AddItemInCart(View):
    def get(self, request, id):
        add_item_to_cart(request, id)
        return redirect('store:auto_parts')


class DeleteItemInCart(View):
    def get(self, request, id):
        delete_item_to_cart(request, id)
        return redirect('store:auto_parts')


class Login(LoginView):
    template_name = 'store/login.html'

    def form_valid(self, form):
        return super().form_valid(form)
