# Generated by Django 3.2 on 2021-04-22 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_remove_autopart_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodywork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Кузов')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Кузов',
                'verbose_name_plural': 'Кузовы',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='EngineType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Тип двигателя')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тип двигателя',
                'verbose_name_plural': 'Типы двигателей',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Meta title')),
                ('meta_description', models.TextField(blank=True, null=True, verbose_name='Meta description')),
                ('meta_keywords', models.TextField(blank=True, null=True, verbose_name='Meta Keywords')),
                ('image', models.ImageField(null=True, upload_to='car', verbose_name='Фотография')),
                ('slug', models.SlugField(unique=True, verbose_name='URL')),
                ('engine_capacity', models.CharField(max_length=255, verbose_name='Объем двигателя')),
                ('transmission', models.CharField(choices=[(None, 'Выберите коробку передач'), ('mechanics', 'Механика'), ('automatic', 'Автомат')], max_length=10, verbose_name='Коробка передач')),
                ('drive', models.CharField(choices=[(None, 'Выберите привод'), ('front', 'Передний привод'), ('rear_drive', 'Задний привод')], max_length=32, verbose_name='Привод')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег')),
                ('year', models.PositiveSmallIntegerField(verbose_name='Год')),
                ('color', models.CharField(max_length=255, verbose_name='Цвет')),
                ('vin', models.CharField(max_length=255, verbose_name='VIN')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Цена')),
                ('bodywork', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.bodywork', verbose_name='Кузов')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.carmodel', verbose_name='Марка автомобиля')),
                ('engine_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.enginetype', verbose_name='Тип двигателя')),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
                'ordering': ['-id'],
            },
        ),
    ]