# Generated by Django 5.1.4 on 2025-04-06 07:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_alter_inventory_cost_price_alter_inventory_gst_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='max_retail_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
