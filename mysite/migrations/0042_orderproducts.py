# Generated by Django 3.2.13 on 2022-06-07 06:54

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion
import mysite.validators


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0041_auto_20220601_1139'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_colour', colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=None, verbose_name='Цвет')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='Размер')),
                ('price', models.PositiveIntegerField(blank=True, null=True, verbose_name='Цена')),
                ('old_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Старая цена')),
                ('amount', models.PositiveIntegerField(default=1, validators=[mysite.validators.validate_amount], verbose_name='Количество')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.product', verbose_name='Товар')),
                ('product_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.productimage', verbose_name='Фото и цвет')),
            ],
            options={
                'verbose_name': 'Товар в корзине',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]
