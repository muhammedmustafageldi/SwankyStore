# Generated by Django 4.2.6 on 2023-10-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=60)),
                ("description", models.CharField(max_length=200)),
                ("price", models.FloatField(max_length=10)),
                ("stock", models.IntegerField()),
                ("image", models.ImageField(upload_to="product_pictures/")),
            ],
        ),
    ]
