# Generated by Django 3.2.13 on 2022-05-30 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0030_footer_footer_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footerlink',
            name='link',
            field=models.URLField(max_length=255, verbose_name='Ссылка'),
        ),
    ]
