# Generated by Django 4.2.6 on 2023-10-23 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0004_customuser"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CustomUser",
        ),
    ]
