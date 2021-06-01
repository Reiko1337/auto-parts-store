from .models import SparePart, Brand, Model, Category, Bodywork, EngineType
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
        model_queryset = kwargs.pop('model_queryset', None)
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = brand_queryset
        self.fields['category'].queryset = category_queryset
        if model_queryset:
            self.fields['model'].queryset = model_queryset

        self.fields['price_from'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_from'].widget.attrs['placeholder'] = 'От'
        self.fields['price_to'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_to'].widget.attrs['placeholder'] = 'До'

    brand = forms.ModelChoiceField(queryset=Brand.objects.none(), to_field_name='slug', required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.none(), to_field_name='slug', required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), to_field_name='slug', required=False)

    price_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    price_to = forms.ChoiceField(widget=forms.TextInput, required=False)


class KitCarFilter(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['price_from'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_from'].widget.attrs['placeholder'] = 'От'
        self.fields['price_to'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_to'].widget.attrs['placeholder'] = 'До'

        self.fields['mileage_from'].widget.attrs['class'] = 'list__filter-input input__form mask__mileage'
        self.fields['mileage_from'].widget.attrs['placeholder'] = 'От'
        self.fields['mileage_to'].widget.attrs['class'] = 'list__filter-input input__form mask__mileage'
        self.fields['mileage_to'].widget.attrs['placeholder'] = 'До'

    brand = forms.ModelChoiceField(queryset=get_brand_car(), to_field_name='slug', required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.none(), to_field_name='slug', required=False)
    year_from = forms.ChoiceField(choices=get_kit_car_year(), required=False)
    year_to = forms.ChoiceField(choices=get_kit_car_year(), required=False)
    mileage_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    mileage_to = forms.ChoiceField(widget=forms.TextInput, required=False)
    transmission = forms.ChoiceField(choices=KitCar.TRANSMISSION[1:], required=False)
    bodywork = forms.ModelChoiceField(queryset=Bodywork.objects.all(), to_field_name='slug', required=False)
    engine_type = forms.ModelChoiceField(queryset=EngineType.objects.all(), to_field_name='slug', required=False)
    drive = forms.ChoiceField(choices=KitCar.DRIVE[1:], required=False)
    engine_capacity_from = forms.ChoiceField(choices=get_kit_car_engine_capacity(), required=False)
    engine_capacity_to = forms.ChoiceField(choices=get_kit_car_engine_capacity(), required=False)
    price_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    price_to = forms.ChoiceField(widget=forms.TextInput, required=False)


class WheelFilter(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price_from'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_from'].widget.attrs['placeholder'] = 'От'
        self.fields['price_to'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_to'].widget.attrs['placeholder'] = 'До'

    brand = forms.ModelChoiceField(queryset=get_brand_car(), to_field_name='slug', required=False)
    model = forms.ModelChoiceField(queryset=Model.objects.none(), to_field_name='slug', required=False)
    material = forms.ChoiceField(choices=get_wheel_material(), required=False)
    diameter = forms.ChoiceField(choices=get_wheel_diameter(), required=False)
    pcd = forms.ChoiceField(choices=get_wheel_pcd(), required=False)
    price_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    price_to = forms.ChoiceField(widget=forms.TextInput, required=False)


class TireFilter(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price_from'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_from'].widget.attrs['placeholder'] = 'От'
        self.fields['price_to'].widget.attrs['class'] = 'list__filter-input input__form mask__price'
        self.fields['price_to'].widget.attrs['placeholder'] = 'До'

    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), to_field_name='slug', required=False)
    season = forms.ChoiceField(choices=Tire.SEASON[1:], required=False)
    diameter = forms.ChoiceField(choices=get_diameter_tire(), required=False)
    width = forms.ChoiceField(choices=get_width_tire(), required=False)
    profile = forms.ChoiceField(choices=get_profile_tire(), required=False)

    price_from = forms.ChoiceField(widget=forms.TextInput, required=False)
    price_to = forms.ChoiceField(widget=forms.TextInput, required=False)
