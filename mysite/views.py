from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import CollectionSerializer, NewsSerializer, PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer, ProductSerializer, FeedbackSerializer, FooterSerializer, FooterLinkSerializer
from .models import Collection, News, PublicOffer, AboutUs, QAImage, QA, Product, Feedback, Footer, FooterLink
from drf_multiple_model.views import ObjectMultipleModelAPIView
from itertools import chain 
from rest_framework.response import Response

@api_view(['POST'])
def new_feedback(request):
    if request.method == 'POST':
        feedback_data = JSONParser().parse(request)
        feedback_serializer = FeedbackSerializer(data=feedback_data)
        if feedback_serializer.is_valid():
            feedback_serializer.save()
            return JsonResponse(feedback_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QAAPIView(APIView):
    pagination_class = None
    querylist = [
        {'queryset': QAImage.objects.all(), 'serializer_class': QAImageSerializer},
        {'queryset': QA.objects.all(), 'serializer_class': QASerializer},
    ]
class ProductDetailView(ObjectMultipleModelAPIView):
    pagination_class = None
    def get_querylist(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        my_product = Product.objects.get(id=pk).collection
        querylist = [
            {'queryset': Product.objects.filter(id=pk),
             'serializer_class': ProductSerializer},
            {'queryset': Product.objects.filter(collection=my_product),
             'serializer_class': ProductSerializer}
        ]
        return querylist
    
    

class ProductView(ObjectMultipleModelAPIView):
    pagination_class = None
    querylist = [
         {'queryset': Product.objects.all(), 'serializer_class': ProductSerializer},
    ]

class FavoriteProductsView(viewsets.ModelViewSet):
    pagination_class = None
    if Product.objects.filter(is_favorite=True).exists() == True:
        queryset = Product.objects.filter(is_favorite=True)
        serializer_class = ProductSerializer
    else:
        # queryset = Product.objects.all().order_by('id')[:1]
        queryset = Product.objects.distinct('collection').all()
        serializer_class = ProductSerializer

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

class FooterViewSet(viewsets.ModelViewSet):
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer

class FooterLinkViewSet(viewsets.ModelViewSet):
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer
