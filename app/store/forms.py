import django_filters
from django.db import models
from .models import AutoPart, WheelDrive


class AutoPartFilter(django_filters.FilterSet):
    class Meta:
        model = WheelDrive
        fields = ['car_model', 'diameter', 'material', 'pcd']
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
