# Generated by Django 3.2 on 2021-06-06 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_model_type_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sparepart',
            name='chapter',
            field=models.CharField(choices=[(None, 'Выберите раздел'), ('car', 'Грузовые'), ('semi-trailer', 'Полуприцепы'), ('trailer', 'Прицепы')], max_length=20, verbose_name='Раздел'),
        ),
    ]
