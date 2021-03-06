# Generated by Django 3.2.13 on 2022-05-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0028_auto_20220530_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(upload_to='', verbose_name='Логотип')),
                ('info', models.CharField(max_length=255, verbose_name='Информация')),
                ('number', models.PositiveIntegerField(verbose_name='Номер в хедере')),
            ],
        ),
        migrations.CreateModel(
            name='FooterLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_type', models.CharField(choices=[('whatsapp', 'Whats app'), ('phone', 'Номер'), ('email', 'Почта'), ('instagram', 'Instagram'), ('telegram', 'Telegram')], max_length=50, verbose_name='Тип')),
                ('link', models.CharField(max_length=255, verbose_name='Ссылка')),
            ],
        ),
    ]
