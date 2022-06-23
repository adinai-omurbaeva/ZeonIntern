from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import (CollectionSerializer, AdvantagesSerializer, NewsSerializer,
                          PublicOfferSerializer, AboutUsSerializer, QAImageSerializer, QASerializer,
                          ProductSerializer, FeedbackSerializer, FooterSerializer, FooterLinkSerializer,
                          OrderSerializer, OrderUserSerializer, FeedbackCreationSerializer,
                          CartProductsSerializer, SearchProductSerialiser)
from .models import (Collection, News, PublicOffer, Advantages, AboutUs, QAImage, QA, Product,
                     Feedback, Footer, FooterLink, OrderProduct, OrderUserInfo, Order, CartProducts,
                     FavoriteHelper)
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
import random


class LargePagination(PageNumberPagination):
    """ Пагинация """
    page_size = 12


class FourPagination(PageNumberPagination):
    """ Пагинация """
    page_size = 4


class FivePagination(PageNumberPagination):
    """ Пагинация """
    page_size = 5


class FeedbackView(generics.ListAPIView):
    """ Обратная связь """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackPostView(generics.CreateAPIView):
    """ Обратная связь (только пост) """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackCreationSerializer


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


class MainPageView(ObjectMultipleModelAPIView):
    """ Главная страница """
    pagination_class = None
    querylist = [
        {'queryset': Product.objects.filter(hit=True)[:8], 'serializer_class': ProductSerializer},
        {'queryset': Product.objects.filter(new=True)[:4], 'serializer_class': ProductSerializer},
        {'queryset': Collection.objects.all()[:4], 'serializer_class': CollectionSerializer},
        {'queryset': Advantages.objects.all()[:4], 'serializer_class': AdvantagesSerializer},
    ]


class ProductView(viewsets.ModelViewSet):
    """ Все продукты """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsFilter(filters.FilterSet):
    """ Класс для фильтрации по названию. Используется в поиске """
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name', ]


class SearchProductView(generics.ListAPIView):
    """ Поиск товара по названию """
    queryset = Product.objects.all()
    serializer_class = SearchProductSerialiser
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['name', ]
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
            serializer = SearchProductSerialiser(final_queryset, many=True)
        else:
            serializer = SearchProductSerialiser(filtered_queryset, many=True)
        return Response({'result': serializer.data})


class FavoriteProductsView(generics.ListAPIView):
    """ Избранное.  """
    serializer_class = ProductSerializer
    pagination_class = None
    """ Рандомизация как в поиске (старые избранные) """
    def list(self, request, *args, **kwargs):
        if Product.objects.filter(is_favorite=True).exists():
            queryset = Product.objects.filter(is_favorite=True)
            serializer = ProductSerializer(queryset, many=True)
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
            serializer = ProductSerializer(queryset, many=True)
        return Response({'result': serializer.data, 'favorites number': favorite_amount})


class ExtraFavoriteProductsView(generics.ListAPIView):
    """ Избранное. Рандомизация как в поиске """
    serializer_class = ProductSerializer
    pagination_class = None
    """ Доп задание. Другая рандомизация """
    def list(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if FavoriteHelper.objects.filter(user=pk).exists():
            fav_queryset = FavoriteHelper.objects.filter(user=pk)
            product_ids = fav_queryset.values_list('product')
            queryset = Product.objects.filter(id__in=product_ids)
            serializer = ProductSerializer(queryset, many=True)
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
            serializer = ProductSerializer(queryset, many=True)
        return Response({'result': serializer.data, 'favorites number': favorite_amount})


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


class FooterViewSet(ObjectMultipleModelAPIView):
    """ Футер """
    pagination_class = None
    serializer_class = FooterSerializer
    querylist = [
        {'queryset': Footer.objects.all(), 'serializer_class': FooterSerializer},
        {'queryset': FooterLink.objects.all(), 'serializer_class': FooterLinkSerializer}]


class CollectionViewSet(generics.ListAPIView):
    """ Коллекции """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class CollectionDetailViewSet(generics.ListAPIView):
    """ Содержимое """
    pagination_class = None
    def list(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        my_collection = Collection.objects.get(id=pk)
        product_list = Product.objects.filter(new=True)[:5]
        new_serializer = ProductSerializer(product_list, many=True)
        if my_collection:
            queryset = Product.objects.filter(collection=my_collection)
            if queryset.exists():
                serializer = ProductSerializer(queryset, many=True)
                return Response({'Detail': serializer.data, '5 new': new_serializer.data})
            else:
                return Response({"Collection is empty": pk, '5 new': new_serializer.data})
        else:
            return Response({"Collection doesn't exists": pk, '5 new': new_serializer.data})


class NewProductsViewSet(generics.ListAPIView):
    """ Новинки """
    pagination_class = FivePagination
    queryset = Product.objects.filter(new=True)
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
            OrderProduct.objects.create(order=new_order,
                                        product_image_fk=p_cart.product_image_fk,
                                        product=p_cart.product,
                                        price=p_cart.price,
                                        old_price=p_cart.old_price,
                                        amount=p_cart.amount)
        CartProducts.objects.all().delete()


class ExtraOrderCreateView(generics.CreateAPIView):
    '''Доп задание создание заказов'''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        new_order = serializer.save()
        for p_cart in CartProducts.objects.filter(user=new_order.user):
            OrderProduct.objects.create(order=new_order,
                                        user=p_cart.user,
                                        product_image_fk=p_cart.product_image_fk,
                                        product=p_cart.product,
                                        price=p_cart.price,
                                        old_price=p_cart.old_price,
                                        amount=p_cart.amount)
        CartProducts.objects.all().delete()


class ExtraOrderHistoryListView(generics.ListAPIView):
    '''Доп задание история заказов'''
    def list(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        queryset = Order.objects.filter(user=pk, status='finished')
        serializer = OrderSerializer(queryset, many=True)
        return Response({'result': serializer.data})


class CartViewSet(generics.ListAPIView):
    """ Корзина """
    def list(self, request, *args, **kwargs):
        """Доп задание с пользователем"""
        pk = self.kwargs.get('pk')
        queryset = CartProducts.objects.filter(user=pk)
        serializer_class = CartProductsSerializer

        amount_lines = 0
        my_price = 0
        my_discount = 0
        my_final = 0
        amount_products = 0
        for item in queryset:
            my_price += item.old_price * item.amount
            my_discount += item.old_price * item.amount - item.price * item.amount
            my_final += item.price * item.amount
            amount_products += item.amount * item.product.amount
            amount_lines += item.amount
        serializer = CartProductsSerializer(queryset, many=True)
        return Response({'result': serializer.data, 'lines': amount_lines, 'products': amount_products,
                         'total_price': my_price, 'discount': my_discount, 'final_price': my_final})


class CartDeleteView(generics.DestroyAPIView):
    """Удаление из корзины по айди продукта"""
    def delete(self, request, pk, userpk, format=None):
        my_product = Product.objects.get(id=pk)
        cart_object = CartProducts.objects.get(product=my_product, user=userpk)
        cart_object.delete()
        return Response({'deleted': my_product.name})


class MainHitView(generics.ListAPIView):
    """ Главная страница хит продаж """
    queryset = Product.objects.filter(hit=True)
    serializer_class = ProductSerializer


class MainNewView(generics.ListAPIView):
    """ Главная страница новинки """
    queryset = Product.objects.filter(new=True)
    serializer_class = ProductSerializer
    pagination_class = FourPagination


class MainCollectionView(generics.ListAPIView):
    """ Главная страница коллекции """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = FourPagination


class MainAdvantagesView(generics.ListAPIView):
    """ Главная страница преимущества (без пагинации тк в админ уже стоит ограничение на 4) """
    queryset = Advantages.objects.all()
    serializer_class = AdvantagesSerializer
