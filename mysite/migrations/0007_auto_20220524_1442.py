# Generated by Django 3.2.13 on 2022-05-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20220524_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.CharField(choices=[('spring', 'Весна'), ('summer', 'Лето'), ('fall', 'Осень'), ('winter', 'Зима'), ('dresses', 'Платья'), ('skirts', 'Юбки')], default='summer', max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='fabric_structure',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='hit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
