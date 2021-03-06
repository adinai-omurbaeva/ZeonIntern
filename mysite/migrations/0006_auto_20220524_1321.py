# Generated by Django 3.2.13 on 2022-05-24 07:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_alter_product_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='old_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
