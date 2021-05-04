from django.contrib import admin
from .models import AddressUser


@admin.register(AddressUser)
class AddressUserAdmin(admin.ModelAdmin):
    pass
