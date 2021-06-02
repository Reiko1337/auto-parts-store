from django.contrib import admin
from .models import AddressUser, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username')
    search_fields = ('email', 'username')
    fieldsets = (
        ('Данные', {
            'fields': (
                'email', 'username', 'last_name', 'first_name', 'patronymic', 'phone_number', 'password', 'date_joined')
        }),
        ('Статус', {
            'fields': ('is_superuser', 'is_staff', 'is_active')
        }),
        ('Активность', {
            'fields': ('last_login',)
        }),
        ('Права доступа', {
            'fields': ('groups', 'user_permissions')
        })
    )


@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_address_title', 'get_user__email', 'get_user__username',)
    search_fields = ('user__username', 'user__email')
    fieldsets = (
        ('Клиент', {
            'fields': ('user',)
        }),
        ('Адрес доставки', {
            'fields': ('last_name', 'first_name', 'patronymic', 'country', 'region', 'city', 'address', 'phone_number')
        }),
    )

    def get_address_title(self, rec):
        return rec.get_title()

    def get_user__email(self, rec):
        return rec.user.email

    def get_user__username(self, rec):
        return rec.user.username

    get_user__email.short_description = 'E-mail Пользователя'
    get_user__username.short_description = 'Имя пользователя'
    get_address_title.short_description = 'Адрес'
