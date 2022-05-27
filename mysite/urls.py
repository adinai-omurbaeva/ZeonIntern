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

router = routers.DefaultRouter()
router.register(r'collections', views.CollectionViewSet)

newsrouter = routers.DefaultRouter()
newsrouter.register(r'news', views.NewsViewSet)

publicoffer_router = routers.DefaultRouter()
publicoffer_router.register(r'public offer', views.PublicOfferViewSet)

aboutus_router = routers.DefaultRouter()
aboutus_router.register(r'about us', views.AboutUsViewSet)

#qa_router = routers.DefaultRouter()
#qa_router.register(r'questions and answers', views.QAAPIView, basename='QAModel')
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/aboutus', include(aboutus_router.urls)),
    path('api/collections', include(router.urls)),
    path('api/news', include(newsrouter.urls)),
    path('api/publicoffer', include(publicoffer_router.urls)),
    path('api/product', views.ProductView.as_view()),
    path('api/qa', views.QAAPIView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]