from django.urls import path, include
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
# router.register(r'User', views.UsersView, basename='user')

urlpatterns = [
   path('', include(router.urls)),
   path('userlist', views.UsersView.as_view()),
   path('createuser', views.AddUserView.as_view()),
]
