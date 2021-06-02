# Generated by Django 3.2 on 2021-06-02 18:39

import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_category_subcategory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_rate', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Курс доллара')),
            ],
        ),
        migrations.AlterModelOptions(
            name='bodywork',
            options={'ordering': ['title'], 'verbose_name': 'Кузов автомобиля', 'verbose_name_plural': 'Кузовы автомобилей'},
        ),
        migrations.AlterModelOptions(
            name='enginetype',
            options={'ordering': ['title'], 'verbose_name': 'Тип двигателя', 'verbose_name_plural': 'Типы двигателей'},
        ),
        migrations.AlterField(
            model_name='category',
            name='subcategory',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('car', 'Автомобили'), ('truck', 'Прицеп/Полуприцеп')], help_text='Выберите одну или несколько подкатегорий', max_length=9, verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='kitcar',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='model',
            name='type_model',
            field=models.CharField(choices=[(None, 'Выберите тип модели'), ('car', 'Легковая'), ('truck', 'Прицеп/Полуприцеп')], max_length=20, verbose_name='Тип модели'),
        ),
        migrations.AlterField(
            model_name='tire',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='wheel',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]