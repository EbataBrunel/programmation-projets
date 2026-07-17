"""eajc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from eab.views import home

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path('eab/', include("eab.urls")),
    path('annee/', include("annee.urls")),
    path('etablisement/', include("etablissement.urls")),
    path('baccalaureat/', include("baccalaureat.urls")),
    path('formation/', include("formation.urls")),
    path('entreprise/', include("entreprise.urls")),
    path('experience/', include("experience.urls")),
    path('competence/', include("competence.urls")),
    path('parcours/', include("parcours.urls")),
    path('forum/', include("forum.urls")),
    path('cours/', include("document.urls")),
    path('annonce/', include("annonce.urls")),
    path('reference/', include("reference.urls")),
    path('lm/', include("lettre_mot.urls")),
    path('chat/', include("chat.urls")),
    path('ptf/', include("portfolio.urls")),
    path('auth/', include("app_auth.urls")),
    path('paypal/', include('paypal.standard.ipn.urls')),
    
]

#if settings.DEBUG:
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
