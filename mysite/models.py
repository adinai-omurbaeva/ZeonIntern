from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from .validators import validate_file_extension, validate_amount
from rest_framework import permissions
from django.contrib import messages


class Collection(models.Model):
    """ 
        Коллекции одежды
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    image = models.ImageField(verbose_name= 'Изображение')
    class Meta:
        verbose_name_plural = 'Коллекции'
        verbose_name = "Коллекция"


class Product(models.Model):
    """ 
        Товар
    """
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
    is_favorite = models.BooleanField(default=False, verbose_name='Избранное')

    """ 
        Подсчет скидки при наличии старой цены
    """
    def save(self, *args, **kwargs):
        if self.old_price != 0 and self.old_price > self.price:
            self.discount = int(self.old_price - self.price)
        super(Product, self).save(*args, **kwargs)

    def get_favorites_amount(self):
        amount = Product.objects.filter(is_favorite=True).count()
        return amount
        
    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = "Товар"
    
    
class ProductImage(models.Model):
    """ 
        Фото и цвет товара
    """
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'images/', verbose_name='Изображение')
    color = ColorField(verbose_name='Цвет')
    def __str__(self):
        return '{} : {}'.format(self.product.name, self.color)
    class Meta:
        verbose_name_plural = 'Изображение и цвет товара'
        verbose_name = "Изображение и цвет товара"


class News(models.Model):
    """ 
        Новости
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    image = models.ImageField(verbose_name='Изображение')
    description = RichTextField(null=True, blank=True, verbose_name='Описание')
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'news'
        verbose_name_plural = 'Новости'
        verbose_name = "Новость"


class QA(models.Model):
    """ 
        Модель помощь (вопросы и ответы)
    """
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    class Meta:
        verbose_name_plural = 'Помощь'
        verbose_name = "Помощь"


class QAImage(models.Model):
    """ 
        Картинка для страницы помощи
    """
    image = models.ImageField(verbose_name='Изображение')
    class Meta:
        verbose_name_plural = 'Изображение страницы помощи'
        verbose_name = "Изображение страницы помощи"


class AboutUs(models.Model):
    """ 
        Модель помощь (вопросы и ответы)
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Описание')
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        verbose_name_plural = 'О нас'
        verbose_name = "О нас"


class AboutUsImage(models.Model):
    """ 
        Изображение для страницы о нас
    """
    aboutus = models.ForeignKey(AboutUs, on_delete=models.CASCADE, verbose_name='Изображения')
    image = models.ImageField(verbose_name='Изображение')
    class Meta:
        verbose_name_plural = 'Изображения'
        verbose_name = "Изображение"


class PublicOffer(models.Model):
    """ 
        Публичная оферта
    """
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = RichTextField(verbose_name='Текст')
    class Meta:
        verbose_name_plural = 'Публичная офферта'
        verbose_name = "Публичная офферта"


class Feedback(models.Model):
    """ 
        Обратная связь
    """
    STATUS_CHOISES = (
        ("yes", 'Да'),
        ("no", 'Нет'),
    )
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    date = models.DateField(verbose_name='Дата',auto_now_add=True, blank=True)
    feedback_type = models.CharField(max_length=255, verbose_name='Тип обращения', default='Обратный звонок', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOISES, verbose_name='Статус', default='no', blank=True)
    class Meta:
        verbose_name_plural = 'Обратная связь'
        verbose_name = "Обратная связь"
    

class MainPage(models.Model):
    """ 
        Главная страница
    """
    link = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    image = models.ImageField(verbose_name='Изображение')
    
    class Meta:
        verbose_name_plural = 'Главная страница'
        verbose_name = "Главная страница"


class Advantages(models.Model):
    """ 
        Наши преимущества
    """
    icon = models.FileField(verbose_name='Изображение',validators=[validate_file_extension])
    title = models.CharField(max_length = 255, verbose_name='Заголовок')
    description = models.CharField(max_length=255,verbose_name='Описание')
    class Meta:
        verbose_name_plural = 'Наши преимущества'
        verbose_name = "Наши преимущества"


class FooterLink(models.Model):
    """ 
        Ссылки для футера
    """
    LINK_CHOISES = (
        ("whatsapp", 'Whats app'),
        ("phone", 'Номер'),
        ("email", 'Почта'),
        ("instagram", 'Instagram'),
        ("telegram", 'Telegram'),
    )
    link_type = models.CharField(max_length=50, choices=LINK_CHOISES, verbose_name='Тип')
    link = models.CharField(max_length=255, verbose_name='Ссылка')
    """ 
        Если тип ссылки whatsapp, то преобразует номер в ссылку
    """
    def save(self, *args, **kwargs):
        if self.link_type == 'whatsapp':
            self.link = 'https://wa.me/'+self.link
            super(FooterLink, self).save(*args, **kwargs)
        else:
            super(FooterLink, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.link_type, self.link)
    class Meta:
        verbose_name_plural = 'Ссылки'
        verbose_name = "Ссылка"
    

class Footer(models.Model):
    """ 
        Футер
    """
    logo = models.ImageField(verbose_name='Логотип')
    info = models.CharField(verbose_name='Информация', max_length=255)
    number = models.PositiveIntegerField(verbose_name='Номер в хедере')
    footer_link = models.ManyToManyField(FooterLink)

    def get_link(self):
        my_dict = {}
        for p in self.footer_link.all():
            my_dict.update({p.link_type:p.link})
        return my_dict
    class Meta:
        verbose_name_plural = 'Футер'
        verbose_name = "Футер"
        
class OrderUserInfo(models.Model):
    """ 
        Информация пользователя при оформлении заказа
    """
    STATUS_CHOISES = (
        ("new", 'Новый'),
        ("confirmed", 'Подтвержден'),
        ("canceled", 'Отменен'),
    )
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    phone = models.IntegerField(verbose_name='Номер телефона')
    country = models.CharField(max_length=255, verbose_name='Страна')
    city = models.CharField(max_length=255, verbose_name='Город')
    date = models.DateField(verbose_name='Дата',auto_now_add=True, blank=True)
    status = models.CharField(choices=STATUS_CHOISES, max_length=50, verbose_name='Статус заказа', blank=True, default='new')
    
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    class Meta:
        verbose_name_plural = 'Информация пользователя'
        verbose_name = "Информация пользователя"
    
        

class CartProducts(models.Model):
    """ 
        Корзина
    """
    product_image_fk = models.ForeignKey(ProductImage, verbose_name="Фото и цвет", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена', null=True, blank=True)
    old_price = models.PositiveIntegerField(default = 0,verbose_name='Старая цена', null=True, blank=True)
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество', validators=[validate_amount])
    def clean(self, *args, **kwargs):
        my_product =  ProductImage.objects.get(id=self.product_image_fk.id).product
        if my_product!= self.product:
            raise ValidationError('Не тот товар')
        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        my_product = Product.objects.get(id=self.product.id)
        self.price = my_product.price
        self.old_price = my_product.old_price
        super(CartProducts, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Корзина'
        verbose_name = "Корзина"


class Order(models.Model):
    """ 
        Заказы
    """
    user = models.ForeignKey(OrderUserInfo, verbose_name='Информация пользователя', on_delete=models.CASCADE)
    amount_lines = models.PositiveIntegerField(verbose_name='Количество линеек', default=0, null = True, blank = True)
    amount_products = models.PositiveIntegerField(verbose_name='Количество товаров', default=0, null = True, blank = True)
    price = models.PositiveIntegerField(verbose_name='Стоимость', default=0, null = True, blank = True)
    discount = models.PositiveIntegerField(verbose_name='Скидка', default=0, null = True, blank = True)
    final_price = models.PositiveIntegerField(verbose_name='Итого к оплате', default=0, null = True, blank = True)
    def save(self, *args, **kwargs):
        cart_query = CartProducts.objects.all()
        my_price = 0
        my_discount = 0
        my_final = 0
        for item in cart_query:
            self.price += item.old_price * item.amount        
            self.discount += item.old_price* item.amount - item.price * item.amount 
            self.final_price  += item.price * item.amount
            self.amount_products += item.amount       
        self.amount_lines = cart_query.count()
        super(Order, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = "Заказ"


class OrderProduct(models.Model):
    """ 
        Заказанные товары
    """
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product_image_fk = models.ForeignKey(ProductImage, verbose_name="Фото и цвет", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(verbose_name='Цена', null=True, blank=True)
    old_price = models.PositiveIntegerField(default = 0,verbose_name='Старая цена', null=True, blank=True)
    amount = models.PositiveIntegerField(default=1, verbose_name='Количество', validators=[validate_amount])
    
    def save(self, *args, **kwargs):
        my_product = Product.objects.get(id=self.product.id)
        self.price = my_product.price
        self.old_price = my_product.old_price
        super(OrderProduct, self).save(*args, **kwargs)
        
    
    class Meta:
        verbose_name_plural = 'Товары в заказе'
        verbose_name = "Товар в заказе"
