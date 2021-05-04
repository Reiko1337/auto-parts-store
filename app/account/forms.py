from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import AddressUser
from store.models import Order


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Пароль',
                                    'autocomplete': 'current-password',
                                })
                                )

    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Подтверждение пароля',
                                    'autocomplete': 'current-password',
                                })
                                )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Имя пользователя',
                'autocomplete': 'off',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Почта',
                'autocomplete': 'off',
            }),
        }


class AddressUserForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = ['last_name', 'first_name', 'patronymic', 'country', 'region', 'city', 'address', 'phone_number',
                  'email']


# class CheckoutForm(forms.Form):
#     text = forms.CharField()
#     address_user = forms.ChoiceField(label='Адрес доставки', widget=forms.Select())
#     shipping_method = forms.ChoiceField(label='Адрес доставки')
#     payment_type = forms.ChoiceField(label='Адрес доставки')


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shipping_method', 'payment_type')
