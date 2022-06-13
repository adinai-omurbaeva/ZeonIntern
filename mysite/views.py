from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import CollectionSerializer,AdvantagesSerializer, NewsSerializer, PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer, ProductSerializer, FeedbackSerializer, FooterSerializer, FooterLinkSerializer, OrderProductSerializer, OrderSerializer, OrderUserSerializer, CartProductsSerializer
from .models import Collection, News, PublicOffer, Advantages, AboutUs, QAImage, QA, Product, Feedback, Footer, FooterLink, OrderProduct, OrderUserInfo, Order, CartProducts
from drf_multiple_model.views import ObjectMultipleModelAPIView
from itertools import chain 
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import random


class LargePaginaton(PageNumberPagination):
    """ Пагинация """ 
    page_size = 12

class FivePagination(PageNumberPagination):
    """ Пагинация """ 
    page_size = 5


class FeedbackView(viewsets.ModelViewSet):
    """ Обратная связь """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class QAAPIView(APIView):
    """ Помощь (вопросы и ответы) """
    pagination_class = None
    querylist = [
        {'queryset': QAImage.objects.all(), 'serializer_class': QAImageSerializer},
        {'queryset': QA.objects.all(), 'serializer_class': QASerializer},
    ]


class ProductDetailView(ObjectMultipleModelAPIView):
    """ Детально о продукте """
    pagination_class = None
    serializer_class = ProductSerializer
    def get_querylist(self, *args, **kwargs):
        if getattr(self, "swagger_fake_view", False):
            return Product.objects.none()
        pk = self.kwargs.get('pk')
        my_product = Product.objects.get(id=pk).collection
        querylist = [
            {'queryset': Product.objects.filter(id=pk),
             'serializer_class': ProductSerializer},
            {'queryset': Product.objects.filter(collection=my_product),
             'serializer_class': ProductSerializer}
        ]
        return querylist
    
    
class MainPageView(APIView):
    """ Главная страница """
    pagination_class = None
    querylist = [
        {'queryset': Product.objects.filter(hit = True)[:8],'serializer_class': ProductSerializer},
        {'queryset': Product.objects.filter(new=True)[:4],'serializer_class': ProductSerializer},
        {'queryset': Collection.objects.all()[:4],'serializer_class': CollectionSerializer},
        {'queryset': Advantages.objects.all()[:4],'serializer_class': AdvantagesSerializer},
        ]


class ProductView(viewsets.ModelViewSet):
    """ Все продукты """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsFilter(filters.FilterSet):
    """ Класс для фильтрации по названию. Используется в поиске """ 
    name = filters.CharFilter(field_name = 'name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', ]


class SearchProductView(generics.ListAPIView):
    """ Поиск товара по названию """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name',]
    filter_class = ProductsFilter
    
    """ Рандомная генерация 5 товаров разных категорий """
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
        else:
            serializer = ProductSerializer(filtered_queryset, many=True)
        return Response({'result':serializer.data})


class FavoriteProductsView(generics.ListAPIView):
    """ Избранное. Рандомизация как в поиске """
    serializer_class = ProductSerializer
    pagination_class = None
    def list(self, request, *args, **kwargs):
        favorite_amount = 0
        if Product.objects.filter(is_favorite=True).exists() == True:
            queryset = Product.objects.filter(is_favorite=True)
            serializer = ProductSerializer(queryset,many=True)
            favorite_amount = Product.objects.filter(is_favorite=True).count()
        else:
            favorite_amount = 0
            collections_id = Collection.objects.values_list('id', flat=True)
            collections_id_randomized = random.sample(list(collections_id), 5)
            product_ids = []
            for my_collection in collections_id_randomized:
                my_product = Product.objects.filter(collection__id=my_collection)
                if my_product.exists():
                    product_ids.append(Product.objects.filter(collection__id=my_collection).first().id)
            queryset = Product.objects.filter(id__in=product_ids)   
            serializer = ProductSerializer(queryset,many=True)
        return Response({'result':serializer.data, 'favorites number': favorite_amount})





class NewsViewSet(generics.ListAPIView):
    """ Новости """
    queryset = News.objects.all().order_by('title')
    serializer_class = NewsSerializer


class PublicOfferViewSet(generics.ListAPIView):
    """ Публичная оферта """
    queryset = PublicOffer.objects.all().order_by('title')
    serializer_class = PublicOfferSerializer


class AboutUsViewSet(generics.ListAPIView):
    """ О нас """
    queryset = AboutUs.objects.all().order_by('title')
    serializer_class = AboutUsSerializer


class FooterViewSet(generics.ListAPIView):
    """ Футер """
    queryset = Footer.objects.all()
    serializer_class = FooterSerializer


class FooterLinkViewSet(generics.ListAPIView):
    """ Получаем ссылки футера """
    queryset = FooterLink.objects.all()
    serializer_class = FooterLinkSerializer


class CollectionViewSet(generics.ListAPIView):
    """ Коллекции """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionDetailViewSet(generics.ListAPIView):
    """ Содержимое """
    pagination_class = None
    serializer_class = ProductSerializer
    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        my_collection = Collection.objects.get(id = pk)
        queryset = Product.objects.filter(collection=my_collection)
        return queryset


class NewProductsViewSet(generics.ListAPIView):
    pagination_class = FivePagination
    queryset = Product.objects.filter(new = True)
    serializer_class = ProductSerializer

class OrderCreateViewSet(viewsets.ModelViewSet):
    """ Создание заказа """
    pagination_class = None
    queryset = OrderUserInfo.objects.all()
    serializer_class = OrderUserSerializer

    def perform_create(self, serializer):
        new_user = serializer.save()
        new_order = Order(user=new_user)
        new_order.save()
        for p_cart in CartProducts.objects.all():
            OrderProduct.objects.create(order = new_order,
                                        product_image_fk=p_cart.product_image_fk,
                                        product=p_cart.product,
                                        price=p_cart.price, 
                                        old_price=p_cart.old_price,
                                        amount=p_cart.amount)
        CartProducts.objects.all().delete()

class CartViewSet(viewsets.ModelViewSet):
    """ Корзина """
    queryset = CartProducts.objects.all()
    serializer_class = CartProductsSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        amount_lines = 0
        my_price = 0
        my_discount = 0
        my_final = 0 
        amount_products = 0
        for item in queryset:
            my_price += item.old_price * item.amount        
            my_discount += item.old_price* item.amount - item.price * item.amount 
            my_final  += item.price * item.amount
            amount_products += item.amount * item.product.amount      
            amount_lines += item.amount
        serializer = CartProductsSerializer(queryset, many=True)
        return Response({'result':serializer.data, 'lines':amount_lines, 'products': amount_products,
                        'total_price':my_price, 'discount': my_discount, 'final_price':my_final})
        