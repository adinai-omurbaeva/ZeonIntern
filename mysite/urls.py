"""zeonsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


router = routers.DefaultRouter()
router.register(r'product', views.ProductView)
router.register(r'feedback', views.FeedbackView)
router.register(r'order', views.OrderCreateViewSet)
# router.register(r'cart', views.CartViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui()),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/aboutus', views.AboutUsViewSet.as_view()),
    path('api/news', views.NewsViewSet.as_view()),
    path('api/publicoffer', views.PublicOfferViewSet.as_view()),
    path('api/qa', views.QAAPIView.as_view()),   
    path('api/footer', views.FooterViewSet.as_view()),
    path('api/favoriteproducts', views.FavoriteProductsView.as_view()),
    path('api/productdetail/<int:pk>', views.ProductDetailView.as_view()),
    path('api/mainpage/', views.MainPageView.as_view()),
    path('api/collectiondetail/<int:pk>/', views.CollectionDetailViewSet.as_view()),
    path('api/newproductslist', views.NewProductsViewSet.as_view()),
    path('api/search/', views.SearchProductView.as_view()),
    path('api/collection/', views.CollectionViewSet.as_view()),
    path('api/cart/', views.CartViewSet.as_view()),
    path('api/cartdelete/<int:pk>', views.CartDeleteView.as_view()),
    path('api/favoriteextra/<int:pk>', views.ExtraFavoriteProductsView.as_view())
]