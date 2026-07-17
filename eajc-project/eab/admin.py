from django.contrib import admin
from .models import*

admin.site.site_header="EAJC"
admin.site.site_title="CV"
admin.site.index_title="EAJC"

class AdminProfile(admin.ModelAdmin):
    list_display=('user','phone','address')
    search_fields=('user',)

class AdminAnnee(admin.ModelAdmin):
    search_fields=('libelle',)

class AdminContact(admin.ModelAdmin):
    list_display=('datecontact','name','email','statut')
    search_fields=('name',)

class AdminParcours(admin.ModelAdmin):
    list_display=('etablissement','formation','niveau')

admin.site.register(Profile, AdminProfile)
admin.site.register(Annee, AdminAnnee)
admin.site.register(Contact, AdminContact)
admin.site.register(Parametre)
