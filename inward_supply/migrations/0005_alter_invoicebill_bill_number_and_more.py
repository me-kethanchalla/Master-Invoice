# Generated by Django 5.1.6 on 2025-03-24 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inward_supply', '0004_alter_productentry_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicebill',
            name='bill_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='phone_number',
            field=models.CharField(max_length=10),
        ),
    ]
