# Generated by Django 3.2.13 on 2022-06-01 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0039_rename_products_favorite_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Избранное',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
