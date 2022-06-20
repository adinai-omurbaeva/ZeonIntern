from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms
from django.shortcuts import redirect
# Register your models here.
from .models import (Product, ProductImage, Order, OrderUserInfo, 
                    OrderProduct, AboutUsImage, CartProducts, News, Collection, QA, 
                    QAImage, AboutUs, PublicOffer, MainPage, Feedback, Footer, FooterLink, 
                    Advantages, FavoriteHelper)
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
    """ Добавление только 1 обьекта в целом """
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(AboutUs, self).has_add_permission(request, obj)
    """ изменение ссылки сразу на страницу добавить или редактировать """
    def changelist_view(self, request, extra_context=None):
        if AboutUs.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            about_us = AboutUs.objects.all().first()
            return redirect(request.path + f"{about_us.id}")

class OrderInlineAdmin(admin.StackedInline):
    extra = 1
    max_num = 8
    model = Order

class OrderProductInline(admin.StackedInline):
    extra = 1
    max_num = 1
    model = OrderProduct

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_lines', 'amount_products', 'price', 'discount', 'final_price')
    inlines = [OrderProductInline,]
    


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_image_fk', 'product', 'price', 'old_price')


# @admin.register(OrderUserInfo)
# class OrderUserAdmin(admin.ModelAdmin):
#     search_fields = ('first_name', 'last_name', 'email', 'phone')
#     list_display = ('first_name', 'last_name', 'phone', 'email', 'country', 'city', 'date', 'status')
#     inlines = [OrderInlineAdmin,]


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
    """ изменение ссылки сразу на страницу добавить или редактировать """
    def changelist_view(self, request, extra_context=None):
        if QAImage.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            qa_image = QAImage.objects.all().first()
            return redirect(request.path + f"{qa_image.id}")


@admin.register(PublicOffer)
class PublicOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(PublicOffer, self).has_add_permission(request, obj)
    def changelist_view(self, request, extra_context=None):
        if PublicOffer.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            public_offer = PublicOffer.objects.all().first()
            return redirect(request.path + f"{public_offer.id}")


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('link','image')
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(MainPage, self).has_add_permission(request, obj)
    def changelist_view(self, request, extra_context=None):
        if MainPage.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            main_page = MainPage.objects.all().first()
            return redirect(request.path + f"{main_page.id}")


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
    list_display = ("info",'logo', 'number')
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        else:
            return True
        return super(Footer, self).has_add_permission(request, obj)
    def changelist_view(self, request, extra_context=None):
        if Footer.objects.all().count() == 0:
            return redirect(request.path + "add/")
        else:
            footer = Footer.objects.all().first()
            return redirect(request.path + f"{footer.id}")

@admin.register(Advantages)
class AdvantagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'description')

@admin.register(FavoriteHelper)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('product', 'user',)

