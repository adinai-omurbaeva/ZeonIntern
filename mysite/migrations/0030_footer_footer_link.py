# Generated by Django 3.2.13 on 2022-05-30 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0029_footer_footerlink'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='footer_link',
            field=models.ManyToManyField(to='mysite.FooterLink'),
        ),
    ]
