from rest_framework.decorators import api_view
from rest_framework.response import Response
from mysite.models import AboutUs
from .serializers import AboutUsSerializer
  
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

@api_view(['POST'])
def add_aboutus(request):
    aboutus = AboutUsSerializer(data=request.data)
  
    # validating for already existing data
    if AboutUs.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
  
    if aboutus.is_valid():
        aboutus.save()
        return Response(aboutus.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)