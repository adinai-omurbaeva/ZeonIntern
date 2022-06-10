from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms

# Register your models here.
from .models import Product, ProductImage, Order, OrderUserInfo, OrderProduct, AboutUsImage, CartProducts, News, Collection, QA, QAImage, AboutUs, PublicOffer, MainPage, Feedback, Footer, FooterLink, Advantages
# from . import models
class CategoryChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "{}".format(obj.name)


class ProductInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 8
    model = ProductImage


class AboutUsInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 3
    model = AboutUsImage


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
 

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title',  'description')
    inlines = [AboutUsInlineAdmin]
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(AboutUs, self).has_add_permission(request, obj)

class OrderInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 8
    model = Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_lines', 'amount_products', 'price', 'discount', 'final_price')
    


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_image_fk', 'product', 'price', 'old_price')


@admin.register(OrderUserInfo)
class OrderUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'email', 'country', 'city', 'date', 'status')
    inlines = [OrderInlineAdmin,]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    get_model_perms = lambda self, req: {}
    

@admin.register(AboutUsImage)
class AboutUsImageAdmin(admin.ModelAdmin):
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


@admin.register(CartProducts)
class CartProductsAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_image_fk',  'price', 'old_price', 'amount')


@admin.register(QAImage)
class QAImageAdmin(admin.ModelAdmin):
    list_display = ('image',)
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(QAImage, self).has_add_permission(request, obj)


@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('link','image')
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(MainPage, self).has_add_permission(request, obj)


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
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(Footer, self).has_add_permission(request, obj)


@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'description')

