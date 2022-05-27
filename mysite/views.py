from django.shortcuts import render
from rest_framework import viewsets

from .serializers import CollectionSerializer, NewsSerializer, PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer, ProductColorSerializer, ProductImageSerializer, ProductSerializer
from .models import Collection, News, PublicOffer, AboutUs, QAImage, QA, ProductImage, ProductColor, Product
from drf_multiple_model.views import ObjectMultipleModelAPIView

class QAAPIView(ObjectMultipleModelAPIView):
    pagination_class = None
    querylist = [
        {'queryset': QAImage.objects.all(), 'serializer_class': QAImageSerializer},
        {'queryset': QA.objects.all(), 'serializer_class': QASerializer},
    ]

class ProductView(ObjectMultipleModelAPIView):
    pagination_class = None
    querylist = [
         {'queryset': Product.objects.all(), 'serializer_class': ProductSerializer},
    ]
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all().order_by('name')
    serializer_class = CollectionSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('title')
    serializer_class = NewsSerializer

class PublicOfferViewSet(viewsets.ModelViewSet):
    queryset = PublicOffer.objects.all().order_by('title')
    serializer_class = PublicOfferSerializer

class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all().order_by('title')
    serializer_class = AboutUsSerializer