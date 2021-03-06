# Generated by Django 3.2.13 on 2022-06-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0048_auto_20220609_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount_lines',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Количество линеек'),
        ),
        migrations.AlterField(
            model_name='order',
            name='amount_products',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Количество товаров'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='order',
            name='final_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Итого к оплате'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Стоимость'),
        ),
    ]
