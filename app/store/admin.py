from django.contrib import admin
from .models import Category, CarModel, CarBrand, AutoPart, Cart, CartContent, WheelDrive, AdditionalPhoto, Car, \
    EngineType, Bodywork, Order, OrderContent
from django.contrib.contenttypes.admin import GenericTabularInline


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
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
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_car_brand__title', 'title')
    list_filter = ('car_brand__title',)
    search_fields = ('car_brand__title', 'title')
    autocomplete_fields = ('car_brand',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('car_brand', 'title')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )

    def get_car_brand__title(self, rec):
        return rec.car_brand.title

    get_car_brand__title.short_description = 'Марка автомобиля'


@admin.register(AutoPart)
class AutoPartAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'car_model', 'in_stock')
    list_filter = ('in_stock', 'car_model__title', 'car_model__car_brand__title')
    search_fields = ('car_model__title', 'car_model__car_brand__title')
    autocomplete_fields = ('car_model',)
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('car_model', 'category', 'article', 'description', 'price', 'in_stock')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )


@admin.register(WheelDrive)
class WheelDriveAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'car_model', 'title', 'in_stock')
    list_filter = ('in_stock', 'car_model__title', 'car_model__car_brand__title')
    search_fields = ('car_model__title', 'car_model__car_brand__title')
    autocomplete_fields = ('car_model',)
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': (
                'car_model', 'title', 'diameter', 'material', 'pcd', 'description', 'article', 'price', 'in_stock')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = ()
    list_display = ('id', 'customer')
    search_fields = ('customer',)


@admin.register(CartContent)
class CartContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Bodywork)
class BodyworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'car_model', 'year', 'vin', 'in_stock')
    list_filter = ('in_stock', 'car_model__title', 'car_model__car_brand')
    search_fields = ('car_model__title', 'car_model__car_brand__title', 'vin')
    autocomplete_fields = ('car_model',)
    readonly_fields = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('car_model', 'bodywork', 'transmission', 'drive', 'vin', 'in_stock')
        }),
        ('Двигатель', {
            'fields': ('engine_type', 'engine_capacity')
        }),
        ('Характеристики', {
            'fields': ('mileage', 'year', 'color', 'price', 'description')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_description')
        })
    )


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_title', 'meta_keywords', 'meta_description')
        })
    )


class OrderContentPanel(admin.TabularInline):
    model = OrderContent
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderContentPanel,)
    list_display = ('user', 'data_place', 'get_status_display')
    readonly_fields = ('data_place',)
    fieldsets = (
        ('Клиент', {
            'fields': ('user', 'address_user')
        }),
        ('Подробности заказа', {
            'fields': ('shipping_method', 'payment_type', 'price')
        }),
        ('Статус', {
            'fields': ('status', 'data_place')
        })
    )


@admin.register(OrderContent)
class OrderContentAdmin(admin.ModelAdmin):
    list_display = ('order', 'title')


admin.site.site_title = 'Разборка в Молодечно'
admin.site.site_header = 'Разборка в Молодечно'
