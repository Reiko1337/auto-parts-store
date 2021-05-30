from django.contrib import admin
from .models import Category, Model, Brand, SparePart, Cart, CartContent, Wheel, AdditionalPhoto, KitCar, \
    EngineType, Bodywork, Order, OrderContent, Manufacturer, Tire
from django.contrib.contenttypes.admin import GenericTabularInline
from .forms import SparePartAdminForm, BrandModelFilterAdminForm


class ModelPanel(admin.TabularInline):
    """Панель моделей"""
    model = Model
    fields = ('title', 'type_model', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    extra = 1
    ordering = ['title']


class AdditionalPhotoPanel(GenericTabularInline):
    """Панель доп. фото"""
    model = AdditionalPhoto
    extra = 1


class CartContentPanel(admin.TabularInline):
    """Панель содержимого корзины"""
    model = CartContent
    extra = 0


class OrderContentPanel(admin.TabularInline):
    """Панель содержимого заказа"""
    model = OrderContent
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ панель (Категория)"""
    list_display = ('id', 'title', 'get_subcategory_display')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'subcategory')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_description', 'meta_keywords')
        })
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Админ панель (Марка (автомобиля/прицепа))"""
    list_display = ('id', 'title')
    list_filter = ('title',)
    search_fields = ('title',)
    inlines = (ModelPanel,)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_description', 'meta_keywords')
        })
    )


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    """Админ панель (Модель автомобиля)"""
    list_display = ('id', 'get_brand__title', 'title', 'type_model')
    list_filter = ('brand__title',)
    search_fields = ('brand__title', 'title')
    autocomplete_fields = ('brand',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('brand', 'title', 'type_model')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Meta', {
            'fields': ('meta_keywords', 'meta_description')
        })
    )

    def get_brand__title(self, rec):
        return rec.brand.title

    get_brand__title.short_description = 'Марка'


@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    """Админ панель (Запчасти)"""
    change_form_template = 'admin/spare_part_change_form.html'
    inlines = (AdditionalPhotoPanel,)
    form = SparePartAdminForm
    list_display = ('id', 'get_brand_and_model_title', 'category', 'chapter', 'in_stock')
    list_filter = ('in_stock', 'model__title', 'model__brand__title')
    search_fields = ('model__title', 'model__brand__title')
    readonly_fields = ('slug',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('chapter', 'brand', 'model', 'category', 'article', 'description', 'price', 'in_stock')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_description', 'meta_keywords')
        })
    )

    def get_brand_and_model_title(self, rec):
        return '{0} {1}'.format(rec.model.brand.title, rec.model.title)

    get_brand_and_model_title.short_description = 'Марка и модель'


@admin.register(Wheel)
class WheelAdmin(admin.ModelAdmin):
    """Админ панель (Диски)"""
    change_form_template = 'admin/bran_model_filter_change_form.html'
    form = BrandModelFilterAdminForm
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'get_brand_and_model_title', 'title', 'in_stock')
    list_filter = ('in_stock', 'model__title', 'model__brand__title')
    search_fields = ('model__title', 'model__brand__title')
    readonly_fields = ('slug',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (
                'brand', 'model', 'title', 'diameter', 'material', 'pcd', 'description', 'article', 'price', 'in_stock')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_keywords', 'meta_description')
        })
    )

    def get_brand_and_model_title(self, rec):
        return '{0} {1}'.format(rec.model.brand.title, rec.model.title)

    get_brand_and_model_title.short_description = 'Марка и модель'


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Админ панель (Производитель шин)"""
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
            'fields': ('meta_keywords', 'meta_description')
        })
    )


@admin.register(Tire)
class TireAdmin(admin.ModelAdmin):
    """Админ панель (Шины)"""
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'manufacturer', 'season', 'get_title', 'in_stock')
    list_filter = ('in_stock', 'manufacturer__title', 'season', 'diameter', 'width', 'profile')
    search_fields = ('manufacture__title', 'season', 'diameter', 'width', 'profile')
    autocomplete_fields = ('manufacturer',)
    readonly_fields = ('slug',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': (
                'manufacturer', 'season', 'diameter', 'width', 'profile', 'description', 'article', 'price', 'in_stock')
        }),
        ('URL', {
            'fields': ('slug',)
        }),
        ('Фотографии', {
            'fields': ('image',)
        }),
        ('Meta', {
            'fields': ('meta_keywords', 'meta_description')
        })
    )

    def get_title(self, rec):
        return '{0}/{1} R{2}'.format(rec.width, rec.profile, rec.diameter)

    get_title.short_description = 'Шина'


@admin.register(Bodywork)
class BodyworkAdmin(admin.ModelAdmin):
    """Админ панель (Кузов автомобиля)"""
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
            'fields': ('meta_keywords', 'meta_description')
        })
    )


@admin.register(EngineType)
class EngineTypeAdmin(admin.ModelAdmin):
    """Админ панель (Тип двигателя)"""
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
            'fields': ('meta_description', 'meta_keywords')
        })
    )


@admin.register(KitCar)
class KitCarAdmin(admin.ModelAdmin):
    """Админ панель (Машинокомплект)"""
    change_form_template = 'admin/bran_model_filter_change_form.html'
    form = BrandModelFilterAdminForm
    inlines = (AdditionalPhotoPanel,)
    list_display = ('id', 'get_brand_and_model_title', 'year', 'vin', 'in_stock')
    list_filter = ('in_stock', 'model__title', 'model__brand')
    search_fields = ('model__title', 'model__brand__title', 'vin')
    readonly_fields = ('slug',)
    save_on_top = True
    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'bodywork', 'transmission', 'drive', 'vin', 'in_stock')
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
            'fields': ('meta_description',)
        })
    )

    def get_brand_and_model_title(self, rec):
        return '{0} {1}'.format(rec.model.brand.title, rec.model.title)

    get_brand_and_model_title.short_description = 'Марка и модель'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ панель (Корзина пользователя)"""
    list_display = ('id', 'get_customer__email', 'get_customer__username')
    search_fields = ('customer',)
    inlines = (CartContentPanel,)

    def get_customer__email(self, rec):
        return rec.customer.email

    def get_customer__username(self, rec):
        return rec.customer.username

    get_customer__email.short_description = 'E-mail Пользователя'
    get_customer__username.short_description = 'Имя пользователя'


@admin.register(CartContent)
class CartContentAdmin(admin.ModelAdmin):
    """Админ панель (Содержимое корзины пользователя)"""
    list_display = ('get_content_type_model_name', 'get_content_object_title')

    def get_content_type_model_name(self, rec):
        return rec.content_type.name

    def get_content_object_title(self, rec):
        return rec.content_object.get_title()

    get_content_type_model_name.short_description = 'Модель'
    get_content_object_title.short_description = 'Товар'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Админ панель (Заказ)"""
    inlines = (OrderContentPanel,)
    list_display = ('id', 'get_user__email', 'user', 'data_place', 'get_status_display')
    readonly_fields = ('data_place',)
    fieldsets = (
        ('Клиент', {
            'fields': ('user',)
        }),
        ('Адрес доставки', {
            'fields': ('last_name', 'first_name', 'patronymic', 'country', 'region', 'city', 'address', 'phone_number')
        }),
        ('Подробности заказа', {
            'fields': ('shipping_method', 'payment_type', 'price')
        }),
        ('Статус', {
            'fields': ('status', 'data_place')
        })
    )

    def get_user__email(self, rec):
        return rec.user.email

    get_user__email.short_description = 'E-mail Пользователя'


@admin.register(OrderContent)
class OrderContentAdmin(admin.ModelAdmin):
    """Админ панель (Содержимое заказа)"""
    list_display = ('order', 'title', 'price')


admin.site.site_title = 'Разборка в Молодечно'
admin.site.site_header = 'Разборка в Молодечно'
