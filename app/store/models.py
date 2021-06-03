from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from multiselectfield import MultiSelectField


class MetaTag(models.Model):
    """Мета теги"""
    meta_description = models.TextField(verbose_name='Meta description', null=True, blank=True,
                                        help_text='Meta Description – это одиночный тег, '
                                                  'содержащий краткое описание web-страницы, '
                                                  'используемое при формировании сниппета. '
                                                  'Данный тег в значительной степени влияет на '
                                                  'представление сайта в результатах поисковой выдачи, '
                                                  'и рекомендуется к заполнению поисковыми системами.')
    meta_keywords = models.TextField(verbose_name='Meta Keywords', null=True, blank=True,
                                     help_text='Meta keywords — список ключевых слов , '
                                               'соответствующих содержимому страницы сайта.')

    class Meta:
        abstract = True


class Category(MetaTag):
    """Категория"""
    SUBCATEGORY = (
        ('car', 'Автомобили'),
        ('truck', 'Прицеп/Полуприцеп')
    )
    title = models.CharField(verbose_name='Название', max_length=255, db_index=True)

    subcategory = MultiSelectField(verbose_name='Подкатегория', choices=SUBCATEGORY,
                                   help_text='Выберите одну или несколько подкатегорий')

    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class Brand(MetaTag):
    """Марка (автомобиля/прицепа)"""
    title = models.CharField(verbose_name='Марка', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Марка (автомобиля/прицепа)'
        verbose_name_plural = 'Марки (автомобиля/прицепа)'
        ordering = ['title']

    def __str__(self):
        return self.title


class Model(MetaTag):
    """Модель (автомобиля/прицепа)"""
    TYPE_MODEL = (
        (None, 'Выберите тип модели'),
        ('car', 'Легковая'),
        ('truck', 'Прицеп/Полуприцеп')
    )

    brand = models.ForeignKey(Brand, verbose_name='Марка', on_delete=models.CASCADE, db_index=True)
    title = models.CharField(verbose_name='Модель', max_length=255)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    type_model = models.CharField(verbose_name='Тип модели', choices=TYPE_MODEL, max_length=20)

    class Meta:
        verbose_name = 'Модель (автомобиля/прицепа)'
        verbose_name_plural = 'Модели (автомобиля/прицепа)'
        ordering = ['title']

    def __str__(self):
        return self.title


class SparePart(MetaTag):
    """Запчасти"""
    CHAPTER = (
        (None, 'Выберите раздел'),
        ('car', 'Легковые'),
        ('semi-trailer', 'Полуприцепы'),
        ('trailer', 'Прицепы')
    )

    chapter = models.CharField(verbose_name='Раздел', max_length=20, choices=CHAPTER)
    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='spare_parts', default='default.png')
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12,
                                validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    favorite = GenericRelation('customer.Favorite')
    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        validation_in_stock_for_cart_content(self.in_stock, self.cart_content.all())
        super().save(*args, **kwargs)
        value = 'spare-part-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_title(self):
        return '{0}'.format(self.category.title)

    def get_price(self):
        exchange = Exchange.objects.first()
        if exchange:
            return round(exchange.currency_rate * self.price, 2)
        return self.price

    def get_category__title(self):
        return '{0}'.format(self.category.title)

    def get_model_name(self):
        return self._meta.model_name

    def get_brand__title(self):
        return self.model.brand.title

    def get_model__title(self):
        return self.model.title

    def get_absolute_url(self):
        return reverse('store:detail_spare_part', kwargs={'brand': self.model.brand.slug,
                                                          'model': self.model.slug,
                                                          'category': self.category.slug,
                                                          'slug': self.slug})

    def __str__(self):
        return '{0} {1}'.format(self.model, self.category)


class Wheel(MetaTag):
    """Диски"""
    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='wheel', default='default.png')
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    diameter = models.PositiveSmallIntegerField(verbose_name='Диаметр')
    material = models.CharField(verbose_name='Материал', max_length=255)
    pcd = models.CharField(verbose_name='PCD', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    favorite = GenericRelation('customer.Favorite')
    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Диски'
        verbose_name_plural = 'Диски'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        validation_in_stock_for_cart_content(self.in_stock, self.cart_content.all())
        super().save(*args, **kwargs)
        value = 'wheel-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_title(self):
        return self.title

    def get_price(self):
        exchange = Exchange.objects.first()
        if exchange:
            return round(exchange.currency_rate * self.price, 2)
        return self.price

    def get_model_name(self):
        return self._meta.model_name

    def get_brand__title(self):
        return self.model.brand.title

    def get_model__title(self):
        return self.model.title

    def get_absolute_url(self):
        return reverse('store:detail_wheel', kwargs={'brand': self.model.brand.slug,
                                                     'model': self.model.slug,
                                                     'slug': self.slug})

    def __str__(self):
        return '{0} {1}'.format(self.model, self.title)


class Manufacturer(MetaTag):
    """Производитель шин"""
    title = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Производитель шин'
        verbose_name_plural = 'Производители шин'
        ordering = ['-title']

    def __str__(self):
        return self.title


class Tire(MetaTag):
    """Шины"""
    SEASON = (
        (None, 'Выберите сезон'),
        ('summer', 'Летний'),
        ('winter', 'Зимний'),
        ('all-season', 'Всесезонный')
    )

    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', on_delete=models.CASCADE)
    season = models.CharField(verbose_name='Сезон', max_length=20, choices=SEASON)
    diameter = models.DecimalField(verbose_name='Диаметр', decimal_places=1, max_digits=3)
    width = models.DecimalField(verbose_name='Ширина', decimal_places=1, max_digits=4)
    profile = models.DecimalField(verbose_name='Профиль', decimal_places=1, max_digits=3)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='tire', default='default.png')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    favorite = GenericRelation('customer.Favorite')
    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Шины'
        verbose_name_plural = 'Шины'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        validation_in_stock_for_cart_content(self.in_stock, self.cart_content.all())
        super().save(*args, **kwargs)
        value = 'tire-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_title(self):
        return 'Шины {0}/{1} R{2}'.format(self.width, self.profile, self.diameter)

    def get_price(self):
        exchange = Exchange.objects.first()
        if exchange:
            return round(exchange.currency_rate * self.price, 2)
        return self.price

    def get_model_name(self):
        return self._meta.model_name

    def get_manufacturer(self):
        return self.manufacturer.title

    def get_absolute_url(self):
        return reverse('store:detail_tire', kwargs={'slug': self.slug})

    def __str__(self):
        return '{0}/{1} R{2}'.format(self.width, self.profile, self.diameter)


class Bodywork(MetaTag):
    """Кузов автомобиля"""
    title = models.CharField(verbose_name='Кузов', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Кузов автомобиля'
        verbose_name_plural = 'Кузовы автомобилей'
        ordering = ['title']

    def __str__(self):
        return self.title


class EngineType(MetaTag):
    """Тип двигателя"""
    title = models.CharField(verbose_name='Тип двигателя', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тип двигателя'
        verbose_name_plural = 'Типы двигателей'
        ordering = ['title']

    def __str__(self):
        return self.title


class KitCar(MetaTag):
    """Машинокомплект"""

    TRANSMISSION = (
        (None, 'Выберите коробку передач'),
        ('mechanics', 'Механика'),
        ('automatic', 'Автомат')
    )
    DRIVE = (
        (None, 'Выберите привод'),
        ('front', 'Передний привод'),
        ('rear_drive', 'Задний привод')
    )

    model = models.ForeignKey(Model, verbose_name='Модель', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фотография', upload_to='kit-car', default='default.png')
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    bodywork = models.ForeignKey(Bodywork, verbose_name='Кузов', on_delete=models.SET_NULL, null=True)
    engine_type = models.ForeignKey(EngineType, verbose_name='Тип двигателя', on_delete=models.SET_NULL, null=True)
    engine_capacity = models.DecimalField(verbose_name='Объем двигателя', decimal_places=1, max_digits=3)
    transmission = models.CharField(verbose_name='Коробка передач', choices=TRANSMISSION, max_length=10)
    drive = models.CharField(verbose_name='Привод', choices=DRIVE, max_length=32)
    mileage = models.PositiveIntegerField(verbose_name='Пробег')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    color = models.CharField(verbose_name='Цвет', max_length=255)
    vin = models.CharField(verbose_name='VIN', max_length=255, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    favorite = GenericRelation('customer.Favorite')
    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Машинокомплект'
        verbose_name_plural = 'Машинокомплекты'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        validation_in_stock_for_cart_content(self.in_stock, self.cart_content.all())
        super().save(*args, **kwargs)
        value = 'kit-car-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        return super().save(*args, **kwargs)

    def get_title(self):
        return self.model

    def get_price(self):
        exchange = Exchange.objects.first()
        if exchange:
            return round(exchange.currency_rate * self.price, 2)
        return self.price

    def get_model_name(self):
        return self._meta.model_name

    def get_brand__title(self):
        return self.model.brand.title

    def get_model__title(self):
        return self.model.title

    def get_absolute_url(self):
        return reverse('store:detail_kit_car', kwargs={'brand': self.model.brand.slug,
                                                       'model': self.model.slug,
                                                       'slug': self.slug})

    def __str__(self):
        return '{0} {1} {2}'.format(self.model, self.year, self.vin)


class AdditionalPhoto(models.Model):
    """Дополнительные фото"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    image = models.ImageField(verbose_name='Фотография', upload_to='additional_photos', null=True)

    class Meta:
        verbose_name = 'Дополнительное фото'
        verbose_name_plural = 'Дополнительные фото'
        ordering = ['-id']


class Cart(models.Model):
    """Корзина пользователя"""

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'
        ordering = ['-id']

    def get_cart_content(self):
        return self.cartcontent_set.all()

    def get_total_price(self):
        items = self.get_cart_content()
        return sum(item.content_object.get_price() for item in items)

    def get_cart_content_count(self):
        return self.get_cart_content().count()

    def __str__(self):
        return self.customer.username


class CartContent(models.Model):
    """Содержимое корзины"""

    cart = models.ForeignKey(Cart, verbose_name='Корзина пользователя', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        verbose_name = 'Содержимое в корзине'
        verbose_name_plural = 'Содержимое в корзине'
        ordering = ['-id']

    def __str__(self):
        return mark_safe('<a href="/admin/{0}/{1}/{2}/change/">ССЫЛКА</a>'.format(self.content_type.app_label,
                                                                                  self.content_type.model,
                                                                                  self.content_object.pk))


class Order(models.Model):
    """Заказ"""

    STATUS_CHOICES = (
        ('new', 'Новый заказ'),
        ('in_progress', 'Заказ в обработке'),
        ('is_ready', 'Заказ готов'),
        ('completed', 'Заказ выполнен'),
        ('cancel', 'Заказ отменен')
    )
    SHIPPING = (
        (None, 'Выберите способ доставки'),
        ('delivery_by', 'Доставка по Беларуси'),
        ('delivery_ru', 'Доставка в РФ'),
        ('pick_up', 'Самовывоз')
    )
    PAYMENT_TYPE_CHOICES = (
        (None, 'Выберите способ оплаты'),
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('non_cash', 'Безналичный расчет (для юридических лиц)'),
        ('card_halva', 'Карта рассрочки «Халва»'),
        ('card_buy', '«Карта покупок» в рассрочку до 3 месяцев')
    )
    COUNTRY = (
        (None, 'Выберите страну'),
        ('Bel', 'Беларусь'),
        ('ru', 'Россия')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    shipping_method = models.CharField(verbose_name='Доставка', choices=SHIPPING, max_length=24)
    payment_type = models.CharField(max_length=100, verbose_name='Способ оплаты', choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=100, verbose_name='Статус заказ', choices=STATUS_CHOICES, default='new')
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, null=True, blank=True)
    data_place = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    patronymic = models.CharField(verbose_name='Отчество', max_length=255)
    country = models.CharField(verbose_name='Страна', choices=COUNTRY, max_length=16)
    region = models.CharField(verbose_name='Регион', max_length=255)
    city = models.CharField(verbose_name='Город', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']

    def get_order_content(self):
        return self.ordercontent_set.all()

    def get_count(self):
        return self.ordercontent_set.all().count()

    def get_title(self):
        return 'Заказ {0} от {1}'.format(self.pk, self.data_place.strftime('%d.%m.%Y'))

    def __str__(self):
        return '{0} {1} {2}'.format(self.user.username, self.data_place.strftime('%d.%m.%Y'), self.get_status_display())


class OrderContent(models.Model):
    """Содержимое заказа"""

    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название товара', max_length=255)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')

    class Meta:
        verbose_name = 'Содержимое в заказе'
        verbose_name_plural = 'Содержимое в заказе'
        ordering = ['-id']

    def __str__(self):
        return mark_safe('<a href="/admin/{0}/{1}/{2}/change/">ССЫЛКА</a>'.format(self.content_type.app_label,
                                                                                  self.content_type.model,
                                                                                  self.content_object.pk))


class Exchange(models.Model):
    """Курс доллара"""
    currency_rate = models.DecimalField(verbose_name='Курс доллара', decimal_places=2, max_digits=12)

    class Meta:
        verbose_name = 'Курс доллара'
        verbose_name_plural = 'Курс доллара'

    def clean(self):
        if Exchange.objects.count() > 0:
            raise ValidationError('Вы можете создать только одну запись о курсе доллара')

    def __str__(self):
        return 'USD {0}'.format(self.currency_rate)


def validation_in_stock_for_cart_content(in_stock, cart_contents):
    """Проверка содержимого в корзине"""
    if not in_stock:
        for item in cart_contents:
            item.delete()
