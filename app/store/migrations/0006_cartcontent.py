# Generated by Django 3.2 on 2021-04-17 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('store', '0005_auto_20210417_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='Корзина пользователя')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Содержимое в корзине',
                'verbose_name_plural': 'Содержимое в корзине',
                'ordering': ['-id'],
            },
        ),
    ]