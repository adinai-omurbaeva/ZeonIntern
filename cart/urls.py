from django.conf.urls import url
from . import views
from django.urls import include, path


urlpatterns = [
    path('add/<int:pk>/', views.AddToCart.as_view(), name='cart_add'),
    path('', views.GetFromCart.as_view()),
    path('remove/<int:pk>/', views.RemoveFromCart.as_view(), name='cart_remove'),
]