# Generated by Django 5.1.2 on 2024-12-07 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0007_products_price_currency_alter_customers_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
