from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(verbose_name= 'Изображение')
    class Meta:
        verbose_name_plural = 'Коллекции'
        verbose_name = "Коллекция"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, verbose_name='Коллекция')
    articul = models.CharField(max_length=255,verbose_name='Артикул')
    price = models.PositiveIntegerField(verbose_name='Цена')
    old_price = models.PositiveIntegerField(default = 0,verbose_name='Старая цена')
    discount = models.PositiveIntegerField(null=True, blank=True,verbose_name='Скидка')
    description = RichTextField(null=True, blank=True,verbose_name='Описание')
    size = models.CharField(max_length=255, default="42-50",verbose_name='Размер')
    fabric_structure = models.CharField(max_length=255, null=True, blank=True,verbose_name='Состав ткани')
    amount = models.PositiveIntegerField(default = 0,verbose_name='Количество в линейке')
    material = models.CharField(max_length=255, null=True, blank=True,verbose_name='Материал')
    hit = models.BooleanField(default=False,verbose_name='Хит продаж')
    new = models.BooleanField(default=False,verbose_name='Новинки')
    def save(self, *args, **kwargs):
        if self.old_price != 0 and self.old_price > self.price:
            self.discount = int(self.old_price - self.price)
            super(Product, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = "Товар"
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'images/', verbose_name='Изображение')
    class Meta:
        verbose_name_plural = 'Изображения товара'
        verbose_name = "Изображение товара"

class ProductColor(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    color = ColorField(verbose_name='Цвет')
    class Meta:
        verbose_name_plural = 'Цвета товара'
        verbose_name = "Цвет товара"

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Изображение')
    description = RichTextField(null=True, blank=True, verbose_name='Описание')
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'news'
        # Add verbose name
        verbose_name_plural = 'Новости'
        verbose_name = "Новость"


class QA(models.Model):
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    def save(self, *args, **kwargs):
        if not self.pk and QA.objects.exists():
        # if you'll not check for self.pk 
        # then error will also raised in update of exists model
            raise ValidationError('Может существовать только одно изображение')
        return super(QA, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Помощь'
        verbose_name = "Помощь"

class QAImage(models.Model):
    image = models.ImageField(verbose_name='Изображение')
    def save(self, *args, **kwargs):
        if not self.pk and QAImage.objects.exists():
        # if you'll not check for self.pk 
        # then error will also raised in update of exists model
            raise ValidationError('Может существовать только одно изображение')
        return super(QAImage, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Изображение страницы помощи'
        verbose_name = "Изображение страницы помощи"

class AboutUs(models.Model):
    image1 = models.ImageField(verbose_name='Изображение 1')
    image2 = models.ImageField(verbose_name='Изображение 2')
    image3 = models.ImageField(verbose_name='Изображение 3')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Описание')
    def save(self, *args, **kwargs):
        if not self.pk and AboutUs.objects.exists() and AboutUs.objects.all().count()>=4:
        # if you'll not check for self.pk 
        # then error will also raised in update of exists model
            raise ValidationError('Может быть только 4 блока')
        return super(AboutUs, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    class Meta:
        verbose_name_plural = 'О нас'
        verbose_name = "О нас"

class PublicOffer(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Текст')
    class Meta:
        verbose_name_plural = 'Публичная офферта'
        verbose_name = "Публичная офферта"

class Feedback(models.Model):
    STATUS_CHOISES = (
        ("yes", 'Да'),
        ("no", 'Нет'),
    )
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата',auto_now_add=True, blank=True)
    feedback_type = models.CharField(max_length=255, verbose_name='Тип обращения', default='Обратный звонок')
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, verbose_name='Статус', default='no')
    class Meta:
        verbose_name_plural = 'Обратная связь'
        verbose_name = "Обратная связь"
    
class MainPage(models.Model):
    image = models.ImageField(verbose_name='Изображение')
    link = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.pk and MainPage.objects.exists():
            raise ValidationError('Может быть только 1 главная страница')
        return super(MainPage, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Главная страница'
        verbose_name = "Главная страница"

class Advantages(models.Model):
    icon = models.ImageField(verbose_name='Изображение')
    title = models.CharField(max_length = 255, verbose_name='Заголовок')
    description = models.CharField(max_length=255,verbose_name='Описание')
    class Meta:
        verbose_name_plural = 'Главная страница'
        verbose_name = "Главная страница"
