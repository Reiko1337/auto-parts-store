from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from .forms import RegistrationForm
from django.views.generic import CreateView, View
from django.urls import reverse_lazy


class Login(LoginView):
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        return super().form_valid(form)


class RegistrationView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('account:login')
    template_name = 'account/reg.html'


class ProfileView(LoginRequiredMixin, View):
    template_name = 'account/profile.html'

    def get(self, request):
        return render(request, self.template_name)
