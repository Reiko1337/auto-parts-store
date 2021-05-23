from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.text import slugify
from account.models import AddressUser


class MataTag(models.Model):
    """Мета теги"""
    meta_title = models.CharField(verbose_name='Meta title', max_length=255, null=True, blank=True)
    meta_description = models.TextField(verbose_name='Meta description', null=True, blank=True)
    meta_keywords = models.TextField(verbose_name='Meta Keywords', null=True, blank=True)

    class Meta:
        abstract = True


class CarBrand(MataTag):
    """Марка автомобиля"""
    title = models.CharField(verbose_name='Марка автомобиля', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'
        ordering = ['title']

    def __str__(self):
        return self.title


class CarModel(MataTag):
    """Модель автомобиля"""
    car_brand = models.ForeignKey(CarBrand, verbose_name='Марка автомобиля', on_delete=models.CASCADE, db_index=True)
    title = models.CharField(verbose_name='Модель автомобиля', max_length=255)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['title']

    def __str__(self):
        return '{0} {1}'.format(self.car_brand.title, self.title)


class Category(MataTag):
    """Категрия"""
    title = models.CharField(verbose_name='Название категории', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

    def __str__(self):
        return self.title


class AutoPart(MataTag):
    """Запчасти"""
    car_model = models.ForeignKey(CarModel, verbose_name='Марка автомобиля', on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, db_index=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='auto_parts', null=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание')
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, validators=[MinValueValidator(0)],
                                default=0)
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)
    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['-id']

    def __str__(self):
        return '{0} {1}'.format(self.car_model, self.category)

    def get_title(self):
        return '{0}'.format(self.category.title)

    def get_category__title(self):
        return '{0}'.format(self.category.title)

    def get_model_name(self):
        return self._meta.model_name

    def get_car_brand__title(self):
        return self.car_model.car_brand.title

    def get_car_model__title(self):
        return self.car_model.title

    def get_in_stock(self):
        return 'В наличии' if self.in_stock else 'Нет в наличии'

    def get_absolute_url(self):
        return reverse('store:detail_auto_part', kwargs={'brand': self.car_model.car_brand.slug,
                                                         'model': self.car_model.slug,
                                                         'category': self.category.slug,
                                                         'slug': self.slug})

    def save(self, *args, **kwargs):
        value = 'auto-part-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        if not self.in_stock:
            cart_contents = self.cart_content.all()
            for item in cart_contents:
                item.delete()
        super().save(*args, **kwargs)


class WheelDrive(MataTag):
    """Диски"""
    car_model = models.ForeignKey(CarModel, verbose_name='Марка автомобиля', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='wheel_drive', null=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    diameter = models.PositiveSmallIntegerField(verbose_name='Диаметр')
    material = models.CharField(verbose_name='Материал', max_length=255)
    pcd = models.CharField(verbose_name='PCD', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12)
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Диски'
        verbose_name_plural = 'Диски'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        value = 'wheel-drive-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        if not self.in_stock:
            cart_contents = self.cart_content.all()
            for item in cart_contents:
                item.delete()
        super().save(*args, **kwargs)

    def get_title(self):
        return self.title

    def get_in_stock(self):
        return 'В наличии' if self.in_stock else 'Нет в наличии'

    def get_model_name(self):
        return self._meta.model_name

    def get_car_brand__title(self):
        return self.car_model.car_brand.title

    def get_car_model__title(self):
        return self.car_model.title

    def get_absolute_url(self):
        return reverse('store:detail_wheel', kwargs={'brand': self.car_model.car_brand.slug,
                                                            'model': self.car_model.slug,
                                                            'slug': self.slug})

    def __str__(self):
        return '{0} {1}'.format(self.car_model, self.title)


class Bodywork(MataTag):
    """Кузов"""
    title = models.CharField(verbose_name='Кузов', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Кузов'
        verbose_name_plural = 'Кузовы'
        ordering = ['-id']

    def __str__(self):
        return self.title


class EngineType(MataTag):
    """Тип двигателя"""
    title = models.CharField(verbose_name='Тип двигателя', max_length=255, db_index=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)

    class Meta:
        verbose_name = 'Тип двигателя'
        verbose_name_plural = 'Типы двигателей'
        ordering = ['-id']

    def __str__(self):
        return self.title


class Car(MataTag):
    """Автомобиль"""
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

    car_model = models.ForeignKey(CarModel, verbose_name='Марка автомобиля', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Фотография', upload_to='car', null=True)
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
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, null=True, blank=True)
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    cart_content = GenericRelation('CartContent')
    additional_photo = GenericRelation('AdditionalPhoto')

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'
        ordering = ['-id']

    def get_title(self):
        return self.car_model

    def get_in_stock(self):
        return 'В наличии' if self.in_stock else 'Нет в наличии'

    def get_model_name(self):
        return self._meta.model_name

    def get_car_brand__title(self):
        return self.car_model.car_brand.title

    def get_car_model__title(self):
        return self.car_model.title

    def get_absolute_url(self):
        return reverse('store:detail_kit_car', kwargs={'brand': self.car_model.car_brand.slug,
                                                        'model': self.car_model.slug,
                                                        'slug': self.slug})

    def save(self, *args, **kwargs):
        value = 'car-{0}'.format(self.pk)
        self.slug = slugify(value, allow_unicode=True)
        if not self.in_stock:
            cart_contents = self.cart_content.all()
            for item in cart_contents:
                item.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{0} {1} {2}'.format(self.car_model, self.year, self.vin)


class Cart(models.Model):
    """Корзина пользователя"""
    customer = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Корзина пользователя'
        verbose_name_plural = 'Корзины пользователей'
        ordering = ['-id']

    def __str__(self):
        return self.customer.username

    def get_cart_content(self):
        return self.cartcontent_set.all()

    def get_total_price(self):
        items = self.get_cart_content()
        return sum(item.content_object.price for item in items)

    def get_cart_content_count(self):
        return self.get_cart_content().count()


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


class AdditionalPhoto(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
    image = models.ImageField(verbose_name='Фотография', upload_to='additional_photos', null=True)

    class Meta:
        verbose_name = 'Дополнительное фото'
        verbose_name_plural = 'Дополнительные фото'
        ordering = ['-id']


class Order(models.Model):
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
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    address_user = models.ForeignKey(AddressUser, verbose_name='Адрес доставки', on_delete=models.SET_NULL, null=True,
                                     blank=True)
    shipping_method = models.CharField(verbose_name='Доставка', choices=SHIPPING, max_length=24)
    payment_type = models.CharField(max_length=100, verbose_name='Способ оплаты', choices=PAYMENT_TYPE_CHOICES)
    status = models.CharField(max_length=100, verbose_name='Статус заказ', choices=STATUS_CHOICES, default='new')
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, null=True, blank=True)
    data_place = models.DateTimeField(verbose_name='Дата заказа', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']

    def __str__(self):
        return '{0} {1} {2}'.format(self.user.username, self.data_place.strftime('%d.%m.%Y'), self.get_status_display())

    def get_order_content(self):
        return self.ordercontent_set.all()

    def get_count(self):
        return self.ordercontent_set.all().count()


class OrderContent(models.Model):
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
