from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from ckeditor.fields import RichTextField
# Create your models here.

class Product(models.Model):
    COLLECTION_CHOISES = (
        ("spring", 'Весна'),
        ("summer", 'Лето'),
        ("fall", 'Осень'),
        ("winter", 'Зима'),
        ('dresses', 'Платья'),
        ('skirts', 'Юбки'),
    )
    name = models.CharField(max_length=255)
    collection = models.CharField(max_length=10, choices=COLLECTION_CHOISES, default="summer")
    articul = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    old_price = models.PositiveIntegerField(default = 0)
    discount = models.PositiveIntegerField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    size = models.CharField(max_length=255, default="42-50")
    fabric_structure = models.CharField(max_length=255, null=True, blank=True)
    amount = models.PositiveIntegerField(default = 0)
    material = models.CharField(max_length=255, null=True, blank=True)
    hit = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.old_price != 0 and self.old_price > self.price:
            self.discount = int(self.old_price - self.price)
            super(Product, self).save(*args, **kwargs)
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    images = models.ImageField(upload_to = 'images/')

class ProductColor(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    color = ColorField()

class News(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField()
    description = RichTextField(null=True, blank=True)

class Collection(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()

class QA(models.Model):
    question = models.TextField()
    answer = models.TextField()

class QAImage(models.Model):
    image = models.ImageField()

class AboutUs(models.Model):
    image1 = models.ImageField()
    image2 = models.ImageField()
    image3 = models.ImageField()
    title = models.CharField(max_length=255)
    description = RichTextField()

class PublicOffer(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()

class Feedback(models.Model):
    STATUS_CHOISES = (
        ("yes", 'Да'),
        ("no", 'Нет'),
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOISES)


