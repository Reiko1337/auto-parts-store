from .models import SparePart, Brand, Model, Category
from django import forms
from django.db.models import Q
from .services.services import *


class SparePartAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()
        self.fields['category'].queryset = Category.objects.none()

        if 'chapter' in self.data:
            try:
                chapter = self.data.get('chapter')
                if chapter == 'car':
                    model = get_model_car().values('brand')
                    categories = get_category_car()
                else:
                    model = get_model_truck().values('brand')
                    categories = get_category_truck()
                self.fields['brand'].queryset = Brand.objects.filter(pk__in=model).all()
                self.fields['category'].queryset = categories
            except:
                pass
        elif self.instance.pk:
            if self.instance.chapter == 'car':
                model = get_model_car().values('brand')
                categories = get_category_car()
            else:
                model = get_model_truck().values('brand')
                categories = get_category_truck()
            self.fields['brand'].queryset = Brand.objects.filter(pk__in=model).all()
            self.fields['category'].queryset = categories

        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id).order_by('title')
            except:
                pass
        elif self.instance.pk:
            brand = self.instance.model.brand
            self.fields['brand'].initial = brand.pk
            self.fields['model'].queryset = brand.model_set.order_by('title')

    brand = forms.ModelChoiceField(label='Марка', queryset=Brand.objects.none())

    class Meta:
        model = SparePart
        fields = '__all__'


class BrandModelFilterAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()

        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(
                    Q(brand_id=brand_id) & Q(type_model='car')).order_by('title')
            except:
                pass
        elif self.instance.pk:
            brand = self.instance.model.brand
            self.fields['brand'].initial = brand.pk
            self.fields['model'].queryset = brand.model_set.filter(type_model='car').order_by('title')

    brand = forms.ModelChoiceField(label='Марка', queryset=Brand.objects.all())

    class Meta:
        model = SparePart
        fields = '__all__'


class SparePartFilter(forms.Form):

    def __init__(self, *args, **kwargs):
        brand_queryset = kwargs.pop('brand_queryset', None)
        category_queryset = kwargs.pop('category_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = brand_queryset
        self.fields['category'].queryset = category_queryset

        self.fields['price_to'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_to'].widget.attrs['placeholder'] = 'От'
        self.fields['price_from'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_from'].widget.attrs['placeholder'] = 'До'

    brand = forms.ModelChoiceField(queryset=Brand.objects.none(), to_field_name='slug', required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.none(), to_field_name='slug', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), to_field_name='slug', required=False)

    price_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    price_to = forms.ChoiceField(widget=forms.TextInput, required=False)

