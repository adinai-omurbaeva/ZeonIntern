# Generated by Django 3.2.13 on 2022-05-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='images',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
