from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователь"""
    patronymic = models.CharField(verbose_name='Отчество', max_length=255, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255, blank=True, null=True)


class AddressUser(models.Model):
    """Адрес доставки"""
    COUNTRY = (
        (None, 'Выберите страну'),
        ('Bel', 'Беларусь'),
        ('ru', 'Россия')
    )

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    patronymic = models.CharField(verbose_name='Отчество', max_length=255)
    country = models.CharField(verbose_name='Страна', choices=COUNTRY, max_length=16)
    region = models.CharField(verbose_name='Регион', max_length=255)
    city = models.CharField(verbose_name='Город', max_length=255)
    address = models.CharField(verbose_name='Адрес', max_length=255)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=255)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
        ordering = ['-id']

    def get_title(self):
        return '{0}, {1}, {2}, {3}'.format(self.get_country_display(), self.region, self.city, self.address)

    def __str__(self):
        return '{0} {1}. {2}. {3}, {4}, {5}, {6}'.format(self.last_name, self.first_name[0], self.patronymic[0],
                                                         self.get_country_display(), self.region, self.city,
                                                         self.address)
