# Generated by Django 3.2 on 2021-04-17 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_autopart_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autopart',
            name='quantity',
        ),
    ]
