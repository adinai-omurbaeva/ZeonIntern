from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import CollectionSerializer, NewsSerializer, PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer, ProductSerializer, FeedbackSerializer, FooterSerializer,FavoriteSerializer, FooterLinkSerializer
from .models import Collection, News, PublicOffer, AboutUs, QAImage, QA, Product, Feedback, Footer, FooterLink, Favorite
from drf_multiple_model.views import ObjectMultipleModelAPIView


@api_view(['POST'])
def new_feedback(request):
    if request.method == 'POST':
        feedback_data = JSONParser().parse(request)
        feedback_serializer = FeedbackSerializer(data=feedback_data)
        if feedback_serializer.is_valid():
            feedback_serializer.save()
            return JsonResponse(feedback_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
class FavoriteView(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

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