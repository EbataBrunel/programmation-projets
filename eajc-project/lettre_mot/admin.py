from django.contrib import admin
from .models import*

class AdminLm(admin.ModelAdmin):
    search_fields=('type',)


admin.site.register(Lettre_mot, AdminLm)
