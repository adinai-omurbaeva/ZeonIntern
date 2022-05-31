from rest_framework import serializers
from rest_framework.response import Response
from .models import Collection, News, PublicOffer, AboutUs, QA, QAImage, Product, Feedback, ProductImage, Footer, FooterLink, Favorite
from drf_multiple_model.views import ObjectMultipleModelAPIView

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id','name', 'image')

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('image', 'title', 'description')

class PublicOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('title', 'description')

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ('image1', 'image2','image3', 'title', 'description')
    
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
        fields = ('p_image','name', 'collection', 'articul', 'price', 'old_price', 'discount', 'description', 'size', 'fabric_structure', 'amount', 'material', 'hit', 'new')
    def get_p_images(self, newproduct):   
        my_image = ProductImage.objects.filter(product=newproduct)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        return final_image.data

class FavoriteSerializer(serializers.ModelSerializer):
    favorite_products = serializers.SerializerMethodField('get_products')
    class Meta:
        model = Favorite
        fields = ('favorite_products',)
    def get_products(self, favorite):
        my_products = Product.objects.filter(id=favorite.product.id)
        final_product = ProductSerializer(instance=my_products, many=True)
        return final_product.data
class OnlyProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'          
class SameProductSerializer(serializers.ModelSerializer):
    pass

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'images', 'color')
    
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
        fields = ('logo', 'info','number', 'get_link')