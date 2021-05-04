from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm, AddressUserForm, CheckoutForm
from django.views.generic import CreateView, View, ListView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import AddressUser
from django.shortcuts import get_object_or_404
from django.db.models import Q
from store.services import get_cart_auth_user
from store.models import OrderContent, Order, CartContent
from django.db import transaction
from store.session import CartSession


class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        cart = CartSession(self.request)
        super().form_valid(form)
        cart_aut_user = get_cart_auth_user(self.request)
        item_content = [item.content_object for item in cart_aut_user.get_cart_content()]
        for item in cart:
            if not item['item'] in item_content:
                CartContent.objects.create(cart=cart_aut_user, content_object=item['item'])
        return HttpResponseRedirect(self.get_success_url())


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/reg.html'


class ProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class AddressUserView(LoginRequiredMixin, ListView):
    template_name = 'account/address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        return AddressUser.objects.filter(user=self.request.user).all()


class OrderHistory(LoginRequiredMixin, ListView):
    template_name = 'account/order.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).all()


class OrderHistoryDetail(LoginRequiredMixin, DetailView):
    template_name = 'account/order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Order.objects.filter(id=self.kwargs.get('id')).all()


class AddressUserDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        address = get_object_or_404(AddressUser, Q(pk=id) & Q(user=request.user))
        address.delete()
        return redirect('account:address')


class AddressUserAddView(LoginRequiredMixin, CreateView):
    form_class = AddressUserForm
    success_url = reverse_lazy('account:address')
    template_name = 'account/address_add.html'

    def form_valid(self, form):
        address_form = form.save(commit=False)
        address_form.user = self.request.user
        address_form.save()
        return super().form_valid(form)


class AddressUserUpdateView(LoginRequiredMixin, UpdateView):
    model = AddressUser
    form_class = AddressUserForm
    success_url = reverse_lazy('account:address')
    template_name = 'account/address_add.html'
    pk_url_kwarg = 'id'


class CheckoutView(LoginRequiredMixin, View):
    template_name = 'account/checkout.html'

    def get(self, request):
        form = CheckoutForm()
        address_user = AddressUser.objects.filter(user=request.user).all()
        context = {
            'form': form,
            'addresses': address_user
        }
        return render(request, self.template_name, context=context)

    @transaction.atomic
    def post(self, request):
        cart = get_cart_auth_user(request)
        cart_content = cart.get_cart_content()
        form = CheckoutForm(request.POST)
        user = request.user
        address_user_id = request.POST['address_user']
        address_user = AddressUser.objects.filter(Q(user=user) & Q(pk=address_user_id)).first()
        if form.is_valid() and address_user and cart_content:
            order = form.save(commit=False)
            order.user = user
            order.address_user = address_user
            order.price = cart.get_total_price()
            order.save()
            for item in cart_content:
                OrderContent.objects.create(order=order, title=item.content_object.get_title(),
                                            price=item.content_object.price, content_object=item.content_object)
                item.content_object.in_stock = False
                item.content_object.save()
                item.delete()
        else:
            print('False')
        return redirect('account:address')
