# tests.py
from django.test import TestCase
from django.urls import reverse
from .models import Annee

class AnneeViewsTestCase(TestCase):


    def setUp(self):
        # Créer des années pour la base de données de test
        Annee.objects.create(libelle="2025")
        Annee.objects.create(libelle="2026")

    def test_liste_annees_vue(self):
        # Connecter un utilisateur avant de faire la requête GET
        self.client.login(username='gistel', password='Gildas2002@')

        response = self.client.get(reverse('annees'))
        self.assertEqual(response.status_code, 302)
        
        
