from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import AddressUser
from store.models import Order
from django.core.exceptions import ValidationError

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


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['shipping_method'].widget.attrs['class'] = 'order__registration-form-radio'
        self.fields['address_user'].widget.attrs['class'] = 'order__registration-form-radio'
        self.fields['payment_type'].widget.attrs['class'] = 'order__registration-form-radio'
        self.fields['address_user'].queryset = AddressUser.objects.filter(user=user).all()

    SHIPPING = (
        ('delivery_by', 'Доставка по Беларуси'),
        ('delivery_ru', 'Доставка в РФ'),
        ('pick_up', 'Самовывоз')
    )
    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('non_cash', 'Безналичный расчет (для юридических лиц)'),
        ('card_halva', 'Карта рассрочки «Халва»'),
        ('card_buy', '«Карта покупок» в рассрочку до 3 месяцев')
    )

    shipping_method = forms.ChoiceField(widget=forms.RadioSelect(), choices=SHIPPING)
    address_user = forms.ModelChoiceField(widget=forms.RadioSelect(), queryset=AddressUser.objects.all())
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_TYPE_CHOICES)

    class Meta:
        model = Order
        fields = ('shipping_method', 'address_user', 'payment_type')

