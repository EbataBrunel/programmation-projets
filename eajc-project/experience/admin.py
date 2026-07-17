from django.contrib import admin
from .models import*

class AdminExperience(admin.ModelAdmin):
    list_display=('type_exp','entreprise','user')
    search_fields=('type_exp',)
admin.site.register(Experience, AdminExperience)
