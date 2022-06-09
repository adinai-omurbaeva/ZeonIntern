from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import CollectionSerializer,AdvantagesSerializer, NewsSerializer, PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer, ProductSerializer, FeedbackSerializer, FooterSerializer, FooterLinkSerializer
from .models import Collection, News, PublicOffer, Advantages, AboutUs, QAImage, QA, Product, Feedback, Footer, FooterLink
from drf_multiple_model.views import ObjectMultipleModelAPIView
from itertools import chain 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import random


class LargePaginaton(PageNumberPagination):
    page_size = 12

class FivePagination(PageNumberPagination):
    page_size = 5

class ProductsFilter(filters.FilterSet):
    # Пользовательский класс фильтрации товаров
    name = filters.CharFilter(field_name = 'name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', ]


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
    
    
class MainPageView(ObjectMultipleModelAPIView):
    pagination_class = None
    querylist = [
        {'queryset': Product.objects.filter(hit = True)[:8],'serializer_class': ProductSerializer},
        {'queryset': Product.objects.filter(new=True)[:4],'serializer_class': ProductSerializer},
        {'queryset': Collection.objects.all()[:4],'serializer_class': CollectionSerializer},
        {'queryset': Advantages.objects.all()[:4],'serializer_class': AdvantagesSerializer},
        ]


class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SearchProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name',]
    filter_class = ProductsFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(queryset)
        if not filtered_queryset:
            collections_id = Collection.objects.values_list('id', flat=True)
            collections_id_randomized = random.sample(list(collections_id), 5)
            product_ids = []
            for my_collection in collections_id_randomized:
                my_product = queryset.filter(collection__id=my_collection)
                if my_product.exists():
                    product_ids.append(queryset.filter(collection__id=my_collection).first().id)
            final_queryset = queryset.filter(id__in=product_ids)    
        serializer = ProductSerializer(final_queryset, many=True)
        return Response({'collections': collections_id_randomized, 'product_ids':product_ids, 'result':serializer.data})


class FavoriteProductsView(viewsets.ModelViewSet):
    pagination_class = None
    if Product.objects.filter(is_favorite=True).exists() == True:
        queryset = Product.objects.filter(is_favorite=True)
        serializer_class = ProductSerializer
    else:
        collections_id = Collection.objects.values_list('id', flat=True)
        collections_id_randomized = random.sample(list(collections_id), 5)
        product_ids = []
        for my_collection in collections_id_randomized:
            my_product = Product.objects.filter(collection__id=my_collection)
            if my_product.exists():
                product_ids.append(Product.objects.filter(collection__id=my_collection).first().id)
        queryset = Product.objects.filter(id__in=product_ids)   
        serializer_class = ProductSerializer


class CollectionViewSet(viewsets.ModelViewSet):
    pagination_class = LargePaginaton
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


class CollectionDetailViewSet(viewsets.ModelViewSet):
    pagination_class = LargePaginaton
    serializer_class = ProductSerializer
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        my_collection = Collection.objects.get(id = pk)
        queryset = Product.objects.filter(collection=my_collection)
        return queryset


class NewProductsViewSet(viewsets.ModelViewSet):
    pagination_class = FivePagination
    queryset = Product.objects.filter(new = True)
    serializer_class = ProductSerializer