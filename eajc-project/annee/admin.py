from django.contrib import admin
from .models import*

class AdminAnnee(admin.ModelAdmin):
    search_fields=('libelle',)

admin.site.register(Annee, AdminAnnee)
