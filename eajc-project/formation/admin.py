from django.contrib import admin
from .models import*

class AdminFormation(admin.ModelAdmin):
    search_fields=('intitule',)

admin.site.register(Formation, AdminFormation)