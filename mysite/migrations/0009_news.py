# Generated by Django 3.2.13 on 2022-05-24 09:00

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
        ),
    ]
