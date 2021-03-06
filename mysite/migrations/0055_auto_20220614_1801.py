# Generated by Django 3.2.13 on 2022-06-14 12:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0054_auto_20220614_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderUserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=255, verbose_name='Почта')),
                ('phone', models.IntegerField(verbose_name='Номер телефона')),
                ('country', models.CharField(max_length=255, verbose_name='Страна')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('status', models.CharField(blank=True, choices=[('new', 'Новый'), ('confirmed', 'Подтвержден'), ('canceled', 'Отменен')], default='new', max_length=50, verbose_name='Статус заказа')),
            ],
            options={
                'verbose_name': 'Информация пользователя',
                'verbose_name_plural': 'Информация пользователя',
            },
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.orderuserinfo', verbose_name='Информация пользователя'),
        ),
    ]
