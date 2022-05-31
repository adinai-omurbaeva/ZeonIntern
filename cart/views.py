from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from mysite.models import Product, ProductImage
from mysite.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class AddToCart(APIView):
    def post(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.add(product)
        return Response({'success':True})

class GetFromCart(APIView):
    def get(self, request, format=None):
        cart=Cart(request)
        return Response({"data": cart.cart,"total_price": cart.get_total_price(),"old_price": cart.get_old_price(),"status": "success"}) 

class RemoveFromCart(APIView):
    def delete(self, request, pk):
        cart = Cart(request)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product)
        return Response({'success':True})
