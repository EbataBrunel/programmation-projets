# my_project/middlewares/maintenance_middleware.py

from django.shortcuts import redirect
from django.urls import reverse

from eab.models import Parametre

class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Récupérer la première instance de Setting
            setting = Parametre.objects.first()
            
            # Si maintenance_mode est activé et l'URL n'est pas celle de la maintenance
            if setting and setting.maintenance_mode and request.path != reverse('maintenance'):
                return redirect('maintenance')
        except Parametre.DoesNotExist:
            # Si aucun paramètre n'est trouvé, passer sans maintenance
            pass

        response = self.get_response(request)
        return response

