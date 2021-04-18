from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Sum


class MataTag(models.Model):
    """Мета теги"""
    meta_title = models.CharField(verbose_name='Meta title', max_length=255, null=True, blank=True)
    meta_description = models.TextField(verbose_name='Meta description', null=True, blank=True)

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
    title = models.CharField(verbose_name='Название', max_length=255, db_index=True)
    image = models.ImageField(verbose_name='Фотография', upload_to='auto_parts', null=True)
    slug = models.SlugField(verbose_name='URL', unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание')
    article = models.CharField(verbose_name='Артикул', max_length=120, db_index=True, unique=True)
    price = models.DecimalField(verbose_name='Цена', decimal_places=2, max_digits=12, validators=[MinValueValidator(0)],
                                default=0)
    in_stock = models.BooleanField(verbose_name='В наличии', default=True)

    cart_content = GenericRelation('CartContent')

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['-id']

    def save(self, *args, **kwargs):
        if not self.in_stock:
            cart_contents = self.cart_content.all()
            for item in cart_contents:
                item.delete()
        super().save(*args, **kwargs)

    def get_car_brand__title(self):
        return self.car_model.car_brand.title

    def get_car_model__title(self):
        return self.car_model.title

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_absolute_url(self):
        return reverse('store:detail_auto_parts', kwargs={'brand': self.car_model.car_brand.slug,
                                                          'model': self.car_model.slug,
                                                          'auto_part': self.slug})

    def __str__(self):
        return '{0} -> {1}'.format(self.car_model, self.title)


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
