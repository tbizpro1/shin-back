from django.contrib import admin
from django.urls import path
from core.api import api
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),  # Certifique-se de que só está registrado aqui
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
