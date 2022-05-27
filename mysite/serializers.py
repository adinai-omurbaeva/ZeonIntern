from rest_framework import serializers

from .models import Collection, News, PublicOffer, AboutUs, QA, QAImage, Product, ProductColor, ProductImage
from drf_multiple_model.views import ObjectMultipleModelAPIView

class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = ('id','name', 'image')

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('image', 'title', 'description')

class PublicOfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PublicOffer
        fields = ('title', 'description')

class AboutUsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AboutUs
        fields = ('image1', 'image2','image3', 'title', 'description')
    
class QASerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QA
        fields = ('question', 'answer')

class QAImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QAImage
        fields = ('image',)

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    p_image = serializers.SerializerMethodField("get_p_images")
    class Meta:
        model = Product
        fields = ('p_image','name', 'collection', 'articul', 'price', 'old_price', 'discount', 'description', 'size', 'fabric_structure', 'amount', 'material', 'hit', 'new')
    def get_p_images(self, newproduct):
        my_image = ProductImage.objects.filter(product=newproduct.id)
        final_image = ProductImageSerializer(instance = my_image, many = True)
        #return final_image


class ProductColorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('product', 'color')

class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('product', 'images')