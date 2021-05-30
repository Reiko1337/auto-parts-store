from .models import SparePart, Brand, Model, Category
from django import forms
from django.db.models import Q


class SparePartAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['model'].queryset = Model.objects.none()
        self.fields['category'].queryset = Category.objects.none()

        if 'chapter' in self.data:
            try:
                chapter = self.data.get('chapter')
                if chapter == 'car':
                    model = Model.objects.filter(type_model='car').values('brand')
                    categories = Category.objects.filter(subcategory__icontains='car').all()
                else:
                    model = Model.objects.exclude(type_model='car').values('brand')
                    categories = Category.objects.filter(subcategory__icontains='truck').all()
                self.fields['brand'].queryset = Brand.objects.filter(pk__in=model).all()
                self.fields['category'].queryset = categories
            except:
                pass

        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = Model.objects.filter(brand_id=brand_id).order_by('title')
            except:
                pass
        elif self.instance.pk:
            if self.instance.chapter == 'car':
                model = Model.objects.filter(type_model='car').values('brand')
                categories = Category.objects.filter(subcategory__icontains='car').all()
            else:
                model = Model.objects.exclude(type_model='car').values('brand')
                categories = Category.objects.filter(subcategory__icontains='truck').all()
            self.fields['brand'].queryset = Brand.objects.filter(pk__in=model).all()
            brand = self.instance.model.brand
            self.fields['brand'].initial = brand.pk
            self.fields['model'].queryset = brand.model_set.order_by('title')
            self.fields['category'].queryset = categories

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
