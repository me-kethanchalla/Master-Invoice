# Generated by Django 5.1.4 on 2025-03-17 05:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inward_supply', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firm_name', models.CharField(max_length=255)),
                ('person_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('debit', models.FloatField(default=0.0)),
                ('total_sales', models.IntegerField(default=0)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
