from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddressUserForm, CheckoutForm, ProfileUpdate
from django.views.generic import CreateView, View, ListView, UpdateView, DetailView
from store.services.cart_services import get_cart_auth_user
from store.models import OrderContent, Order
from django.db import transaction
from store.session import CartSession
from store.services_auth_user import CartUser
from django.contrib import messages
from allauth.account.views import LoginView
from django.http.response import Http404
from django.urls import reverse_lazy
from .models import AddressUser, User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse

from .services.services import *


class Login(LoginView):
    """Авторизация"""
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        cart = CartSession(self.request)
        login = super().form_valid(form)
        if self.request.user.is_authenticated:
            cart_auth_user = CartUser(self.request)
            for item in cart:
                cart_auth_user.add_to_cart(item['item'])
        return login


def show_404(request):
    """Ошибка 404"""
    raise Http404


class ProfileView(LoginRequiredMixin, View):
    """Профиль пользователя"""
    template_name = 'account/profile.html'

    def get(self, request):
        context = {
            'orders_process': get_order_in_processes(get_orders_user(request))
        }

        return render(request, self.template_name, context)


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    """Профиль пользователя"""
    model = User
    form_class = ProfileUpdate
    success_url = reverse_lazy('account_profile')
    template_name = 'account/profile-update.html'

    def form_valid(self, form):
        messages.success(self.request, 'Данные пользователя изменены')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user


class AddressUserView(LoginRequiredMixin, ListView):
    """Список адресов доставки"""
    template_name = 'account/list-address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return get_addresses_user(self.request)


class AddressUserAddView(LoginRequiredMixin, CreateView):
    """Добавить адрес доставки"""
    form_class = AddressUserForm
    success_url = reverse_lazy('account_profile')
    template_name = 'account/address-add(update).html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Добавить адрес доставки'
        return context

    def form_valid(self, form):
        address_form = form.save(commit=False)
        address_form.user = self.request.user
        address_form.save()
        messages.success(self.request, 'Новый адрес доставки добавлен')
        return super().form_valid(form)

    def get_initial(self):
        user = self.request.user
        return {'last_name': user.last_name, 'first_name': user.first_name}


class AddressUserDeleteView(LoginRequiredMixin, View):
    """Удалить адрес доставки"""

    def get(self, request, id):
        address = get_address_user(request, id)
        address.delete()
        messages.success(request, 'Адрес доставки удален')
        return redirect('address')


class AddressUserUpdateView(LoginRequiredMixin, UpdateView):
    """Редактировать адрес доставки"""
    model = AddressUser
    form_class = AddressUserForm
    success_url = reverse_lazy('address')
    template_name = 'account/address-add(update).html'
    pk_url_kwarg = 'id'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Изменить адрес доставки'
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Адрес доставки изменен')
        return super().form_valid(form)


class OrderHistory(LoginRequiredMixin, ListView):
    """История заказов"""
    template_name = 'account/list-order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return get_orders_user(self.request)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        queryset = self.get_queryset()
        context['orders_process'] = get_order_in_processes(queryset)
        return context


class OrderHistoryDetail(LoginRequiredMixin, DetailView):
    """Информация о заказе"""
    template_name = 'account/order-detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return get_orders_user(self.request)


class CheckoutView(LoginRequiredMixin, View):
    """Оформление заказа"""
    template_name = 'account/order-registration.html'

    def handle_no_permission(self):
        messages.info(self.request, 'Для оформления заказа необходимо авторизоваться')
        return super().handle_no_permission()

    def get(self, request):
        cart = get_cart_auth_user(request)
        if not cart.get_cart_content_count():
            messages.error(request, 'Для оформления заказа необходимо добавить товар в корзину')
            return redirect('store:about')
        form = CheckoutForm(user=request.user)
        context = {
            'form': form,
            'addresses': get_addresses_user(self.request)
        }
        return render(request, self.template_name, context=context)

    @transaction.atomic
    def post(self, request):
        form = CheckoutForm(request.POST, user=request.user)
        cart = get_cart_auth_user(request)
        cart_content = cart.get_cart_content()
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.price = cart.get_total_price()
            order.save()
            add_order_content(cart_content, order)
            messages.success(request, 'Заказ оформлен')
            return redirect('store:about')
        return render(request, self.template_name, {'form': form})


class CheckoutAddressUser(View):
    """Адрес пользователя (AJAX)"""

    def get(self, request, id):

        if request.is_ajax():
            queryset = get_address_user_first(request, id)

            if queryset:
                response = {
                    'last_name': queryset.last_name,
                    'first_name': queryset.first_name,
                    'patronymic': queryset.patronymic,
                    'country': queryset.country,
                    'region': queryset.region,
                    'city': queryset.city,
                    'address': queryset.address,
                    'phone_number': queryset.phone_number,
                }
                return JsonResponse({'address': response}, status=200, safe=False)
            else:
                return JsonResponse({'success': False}, status=404)
        return JsonResponse({'success': False}, status=404)
