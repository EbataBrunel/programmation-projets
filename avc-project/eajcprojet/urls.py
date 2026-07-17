
from django.contrib import admin
from django.urls import path, include
from eajc.views import index
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path('auth/', include("app_auth.urls")),
    path('eajc/', include("eajc.urls")),
    path('projet/', include("projet.urls")),
    path('tache/', include("tache.urls")),
    path('progres/', include("progres.urls")),
    path('depense/', include("depense.urls")),
    path('contribution/', include("contribution.urls")),
    path('participation/', include("participation.urls")),
    path('devise/', include("devise.urls")),
    path('contrat/', include("contrat.urls"))
]

#if settings.DEBUG:
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
