from django.contrib import admin

from .models import Payment, AutorisationPayment, AutorisationPaymentSalle, Notification

admin.site.register(Payment)
admin.site.register(AutorisationPayment)
admin.site.register(AutorisationPaymentSalle)
admin.site.register(Notification)
