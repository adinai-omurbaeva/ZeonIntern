from django.contrib import admin
from django.forms import inlineformset_factory

# Register your models here.
from .models import Product, ProductImage, ProductColor, News, Collection, QA, QAImage, AboutUs, PublicOffer
 
class ProductInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 8
    model = ProductImage

class ProductColorInline(admin.StackedInline):
    extra = 1
    max_num = 8
    model = ProductColor

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    inlines = [ProductInlineAdmin, ProductColorInline]
 
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'description')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

@admin.register(QAImage)
class QAImageAdmin(admin.ModelAdmin):
    list_display = ('image',)

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('image1','image2','image3','title',  'description')

@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')