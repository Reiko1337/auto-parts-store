from django import forms
from ..models import Model, Category, Brand, SparePart
from ..services.services import *


class SparePartAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()
        self.fields['category'].queryset = Category.objects.none()

        if self.instance.pk:
            self.fields['price'].help_text = '{0} BYN'.format(self.instance.get_price())

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

        if self.instance.pk:
            self.fields['price'].help_text = '{0} BYN'.format(self.instance.get_price())

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


class TireFormFilterAdmin(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['price'].help_text = '{0} BYN'.format(self.instance.get_price())

    class Meta:
        model = Tire
        fields = '__all__'
