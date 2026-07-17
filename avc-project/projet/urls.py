from django.urls import path
from .views import *

urlpatterns = [
    
    # Projets personnels
    path('proj_p', proj_p, name='proj_p'),
    path("add_pp", add_pp, name="add_pp"),
    path("edit_pp/<str:id>", edit_pp, name="edit_pp"),
    path("edit_proj_p", edit_proj_p, name="edit_proj_p"),
    path("del_pp/<str:id>", del_pp, name="del_pp"),
    
    # Projets individuels et en groupe
    path('proj_g', proj_g, name='proj_g'),
    path("add_pg", add_pg, name="add_pg"),
    path("edit_pg/<str:id>", edit_pg, name="edit_pg"),
    path("edit_proj_g", edit_proj_g, name="edit_proj_g"),
    path("del_pg/<str:id>", del_pg, name="del_pg"),
    
    path("tri_projet/<str:action>", tri_projet.as_view(), name="tri_projet"),
    path("document-projet/<int:projet_id>", document_projet, name="document_projet"),
    path("document-projet-partage/<int:projet_id>", document_projet_partage, name="document_projet_partage"),
    path("configuration", configuration, name="configuration"),
    path("ajax_detail_projet/<int:id>", ajax_detail_projet, name="ajax_detail_projet"),
    path("visibilite_projet/<int:id>", visibilite_projet, name="visibilite_projet"),
    path("visibilite_tache/<int:id>", visibilite_tache, name="visibilite_tache"),
    path("visibilite_depense/<int:id>", visibilite_depense, name="visibilite_depense"),
    path("visibilite_progres/<int:id>", visibilite_progres, name="visibilite_progres"),
    path("proj_perso_partage", proj_perso_partage, name="proj_perso_partage")
    
    
]
