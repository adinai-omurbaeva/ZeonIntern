# Generated by Django 3.2.13 on 2022-05-31 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0038_auto_20220531_1322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='products',
            new_name='product',
        ),
    ]