from rest_framework import serializers

from .models import Collection, News, PublicOffer, AboutUs, QA, QAImage
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