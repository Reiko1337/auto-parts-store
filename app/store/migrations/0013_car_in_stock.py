# Generated by Django 3.2 on 2021-04-22 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_bodywork_car_enginetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='in_stock',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
    ]
