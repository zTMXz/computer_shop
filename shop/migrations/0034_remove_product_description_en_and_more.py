# Generated by Django 4.1.7 on 2023-04-14 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0033_product_description_en_product_description_ru_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="description_en",),
        migrations.RemoveField(model_name="product", name="description_ru",),
        migrations.RemoveField(model_name="product", name="ph_color_name_en",),
        migrations.RemoveField(model_name="product", name="ph_color_name_ru",),
        migrations.AlterField(
            model_name="product",
            name="created",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 14, 9, 58, 47, 235302)
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 14, 9, 58, 47, 235302)
            ),
        ),
    ]