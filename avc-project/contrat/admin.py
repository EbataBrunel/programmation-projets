from django.contrib import admin

from .models import ContratRemboursement, Remboursement, SignatureContrat, SignatureRemboursement

admin.site.register(ContratRemboursement)
admin.site.register(Remboursement)
admin.site.register(SignatureContrat)
admin.site.register(SignatureRemboursement)