# gimao/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('equipement.api.urls')),
    path('api/', include('demandeIntervention.api.urls')),
    path('api/', include('bonTravail.api.urls')),
    path('api/', include('gestionCompte.api.urls')),
    path('api/', include('gestionDonnee.api.urls')),
    path('api/', include('stock.api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)