from django.contrib import admin
from .models import Category, CarModel, CarBrand, AutoPart, Cart, CartContent, WheelDrive, AdditionalPhoto, Car, \
    EngineType, Bodywork
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',),
                           'meta_title': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description')
        })
    )


class CarModelPanel(admin.TabularInline):
    model = CarModel
    fields = ('title', 'slug', 'meta_title')
    prepopulated_fields = {'slug': ('title',),
                           'meta_title': ('title',)}
    extra = 1
    ordering = ['title']


class AdditionalPhotoPanel(GenericTabularInline):
    model = AdditionalPhoto
    extra = 1


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
    search_fields = ('title',)
    inlines = (CarModelPanel,)
    prepopulated_fields = {'slug': ('title',),
                           'meta_title': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'slug')
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description')
        })
    )


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_car_brand__title', 'title')
    list_filter = ('car_brand__title',)
    search_fields = ('car_brand__title', 'title')
    autocomplete_fields = ('car_brand',)
    prepopulated_fields = {'slug': ('title',),
                           'meta_title': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('car_brand', 'title', 'slug')
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description')
        })
    )

    def get_car_brand__title(self, rec):
        return rec.car_brand.title

    get_car_brand__title.short_description = 'Марка автомобиля'


@admin.register(AutoPart)
class AutoPartAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'car_model')
    list_filter = ('car_model__title', 'car_model__car_brand')
    search_fields = ('car_model__title',)
    autocomplete_fields = ('car_model',)
    prepopulated_fields = {'slug': ('article',)}
    fieldsets = (
        (None, {
            'fields': ('car_model', 'category', 'slug', 'description', 'article', 'price', 'in_stock')
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description')
        })
    )


@admin.register(WheelDrive)
class WheelDriveAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)
    prepopulated_fields = {'slug': ('title',),
                           'meta_title': ('title',)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(CartContent)
class CartContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Bodywork)
class BodyworkAdmin(admin.ModelAdmin):
    pass


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    pass


admin.site.site_title = 'Разборка в Молодечно'
admin.site.site_header = 'Разборка в Молодечно'
