# Generated by Django 4.2.6 on 2023-10-22 16:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(
                max_length=200,
                validators=[django.core.validators.MinValueValidator(70)],
            ),
        ),
    ]