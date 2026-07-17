from django.urls import path
from .views import *

urlpatterns = [
    
    # Projets personnels
    path('taches_p', taches_p, name='taches_p'),
    path("add_tp", add_tp, name="add_tp"),
    path("edit_tp/<str:id>", edit_tp, name="edit_tp"),
    path("edit_tper", edit_tache_p, name="edit_tache_p"),
    path("del_tp/<str:id>", del_tp, name="del_tp"),
    # Projets individuels et en groupe
    path('taches_g', taches_g, name='taches_g'),
    path("add_tg", add_tg, name="add_tg"),
    path("edit_tg/<str:id>", edit_tg, name="edit_tg"),
    path("edit_tgr", edit_tache_g, name="edit_tache_g"),
    path("del_tg/<str:id>", del_tg, name="del_tg"),
    
    path("tri_tache/<str:action>", tri_tache.as_view(), name="tri_tache"),
    path("ajax_devise/<int:projet_id>", ajax_devise, name="ajax_devise")
]
