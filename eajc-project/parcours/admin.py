from django.contrib import admin
from .models import*

class AdminParcours(admin.ModelAdmin):
    list_display=('etablissement','formation','niveau')

admin.site.register(Parcours, AdminParcours)
