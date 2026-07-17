from django.urls import path
from .views import *

urlpatterns = [
    
    # Projets personnels
    path('participations', participations, name='participations'),
    path("add_participation", add_participation, name="add_participation"),
    path("edit_participation/<str:id>", edit_participation, name="edit_participation"),
    path("edit-par", edit_part, name="edit_part"),
    path("del-participation/<str:id>", del_participation, name="del_participation"),
    path("ajax_acteur_participation/<int:projet_id>", ajax_acteur_participation, name="ajax_part_participation"),
    path("ajax_devise/<int:projet_id>", ajax_devise, name="ajax_devise")
    
]
