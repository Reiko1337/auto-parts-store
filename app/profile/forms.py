from django import forms
from .models import AddressUser, User
from store.models import Order


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'patronymic', 'phone_number']


class AddressUserForm(forms.ModelForm):
    class Meta:
        model = AddressUser
        fields = ['last_name', 'first_name', 'patronymic', 'country', 'region', 'city', 'address', 'phone_number']


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['shipping_method'].widget.attrs['class'] = 'order__registration-form-radio'
        self.fields['payment_type'].widget.attrs['class'] = 'order__registration-form-radio'

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
    payment_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_TYPE_CHOICES)

    class Meta:
        model = Order
        fields = (
            'shipping_method', 'payment_type', 'last_name', 'first_name', 'patronymic', 'country',
            'region',
            'city', 'address', 'phone_number')
