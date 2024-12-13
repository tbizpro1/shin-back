from django.contrib import admin
from django.urls import path
from core.api import api
from django.conf.urls.static import static
from django.conf import settings
from django.http import HttpResponse  # Adicionada a importação para HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),  
    path('', lambda request: HttpResponse("API is running!", content_type="text/plain")),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
