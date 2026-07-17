from django.contrib import admin
from .models import*

class AdminCompetence(admin.ModelAdmin):
    list_display=('name','user')
    search_fields=('type_comp',)

admin.site.register(Competence, AdminCompetence)
