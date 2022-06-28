from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mysite.urls')),
    # path(r'', include('ckeditor_uploader.urls')),  
   path('firebase/', include('accounts.urls')),
]+ static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
