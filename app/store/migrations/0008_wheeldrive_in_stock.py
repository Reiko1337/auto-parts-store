# Generated by Django 3.2 on 2021-04-19 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_wheeldrive'),
    ]

    operations = [
        migrations.AddField(
            model_name='wheeldrive',
            name='in_stock',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
    ]
