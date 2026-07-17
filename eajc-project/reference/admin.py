from django.contrib import admin
from .models import*

class AdminReference(admin.ModelAdmin):
    search_fields=('name',)

admin.site.register(Reference, AdminReference)