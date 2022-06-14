from rest_framework import serializers
from rest_framework.response import Response
from .models import Collection, News, AboutUsImage, PublicOffer, AboutUs, QA, QAImage, Product, Advantages, Feedback, ProductImage, Footer, FooterLink, OrderUserInfo, OrderProduct, Order, CartProducts
from drf_multiple_model.views import ObjectMultipleModelAPIView
from colorfield.fields import ColorField

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id','name', 'image')

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'description')

class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('title', 'description')

class AboutUsSerializer(serializers.ModelSerializer):
    about_image = serializers.SerializerMethodField("get_images")
    class Meta:
        model = AboutUs
        fields = ('about_image', 'title', 'description')

    """ Получаем все фото """   
    def get_images(self, about):   
        my_image = AboutUsImage.objects.filter(aboutus=about)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        return final_image.data
        
    
class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QA
        fields = ('question', 'answer')

class QAImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = QAImage
        fields = ('image',)

class ProductSerializer(serializers.ModelSerializer):
    p_image = serializers.SerializerMethodField("get_p_images")
    class Meta:
        model = Product
        fields = ('p_image','name', 'collection', 'articul', 'price', 'old_price', 'discount', 'description', 'size', 'fabric_structure', 'amount', 'material', 'hit', 'new', 'is_favorite')
    """ Получаем все фото """ 
    def get_p_images(self, newproduct):   
        my_image = ProductImage.objects.filter(product=newproduct)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        return final_image.data

class FavoriteProductSerializer(serializers.ModelSerializer):
    p_image = serializers.SerializerMethodField("get_p_images")
    class Meta:
        model = Product
        fields = ('p_image','name', 'price', 'old_price', 'size', 'is_favorite','get_favorites_amount')
    """ Получаем все фото """ 
    def get_p_images(self, newproduct):   
        my_image = ProductImage.objects.filter(product=newproduct)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        return final_image.data
    


class OnlyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'          

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'images', 'color')

class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = ('aboutus', 'image')

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'date', 'feedback_type', 'status')

class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta: 
        model = FooterLink
        fields = ('link_type', 'link')

class FooterSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Footer
        fields = ('logo', 'info','number')

class AdvantagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advantages
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderUserInfo
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

class CartProductsSerializer(serializers.ModelSerializer):
    p_image = serializers.SerializerMethodField("get_p_images")
    p_name = serializers.CharField(source='product.name')
    p_size = serializers.CharField(source='product.size')
    class Meta:    
        model = CartProducts
        fields = ('product_image_fk', 'p_image', 'product', 'p_name', 'p_size', 'price', 'old_price','amount')
    def get_p_images(self, newproduct):   
        image_id = CartProducts.objects.get(id = newproduct.id)
        my_image = ProductImage.objects.filter(id = image_id.product_image_fk.id)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        return final_image.data
    