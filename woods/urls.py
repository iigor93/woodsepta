from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from woods import settings

urlpatterns = [
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('admin_panel/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL)
