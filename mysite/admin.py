from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms

# Register your models here.
from .models import Product, ProductImage, News, Collection, QA, QAImage, AboutUs, PublicOffer, MainPage, Feedback, Footer, FooterLink

class CategoryChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "{}".format(obj.name)
         
class ProductInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 8
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'collection':
            return CategoryChoiceField(queryset=Collection.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    inlines = [ProductInlineAdmin,]
    search_fields = ('name', 'price')
    list_filter = ('name', 'price')
    ordering = ('name', 'price')
    
    class Meta:
       model = Product
 
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    get_model_perms = lambda self, req: {}
    

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

@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('image', 'link')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','date','feedback_type', 'status')
    search_fields = ('name', 'phone')
    list_filter = ('status',)
    ordering = ('date', 'name')

@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('link_type', 'link',)

@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ("info",'logo', 'number','get_link')
  