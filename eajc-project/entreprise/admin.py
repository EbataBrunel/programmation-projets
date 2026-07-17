from django.contrib import admin
from .models import*

class AdminEntreprise(admin.ModelAdmin):
    list_display=('name','country','city')
    search_fields=('name',)

admin.site.register(Entreprise, AdminEntreprise)
