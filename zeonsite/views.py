from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from pyrebase import pyrebase

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by title': '/?title=title_aboutus',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/aboutus/pk/delete'
    }
    return Response(api_urls)