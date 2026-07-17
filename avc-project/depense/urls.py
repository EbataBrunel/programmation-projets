from django.urls import path
from .views import *

urlpatterns = [
    
    # Projets personnels
    path('depense_projet_p', depense_projet_p, name='depense_projet_p'),
    path('depense_tache_p/<str:projet_id>', depense_tache_p, name='depense_tache_p'),
    path("add_depense_p", add_depense_p, name="add_depense_p"),
    path("edit_depense_p/<str:id>", edit_depense_p, name="edit_depense_p"),
    path("edit-dep_p", edit_dep_p, name="edit_dep_p"),
    path("del-depense_p/<str:id>", del_depense_p, name="del_depense_p"),
    
    # Projets individuels et en groupe
    path('depense_projet_g', depense_projet_g, name='depense_projet_g'),
    path('depense_tache_g/<str:projet_id>', depense_tache_g, name='depense_tache_g'),
    path("add_depense_g", add_depense_g, name="add_depense_g"),
    path("edit_depense_g/<str:id>", edit_depense_g, name="edit_depense_g"),
    path("edit_dep_g", edit_dep_g, name="edit_dep_g"),
    path("del_depense_g/<str:id>", del_depense_g, name="del_depense_g"),
    
    path("tri_depense/<str:action>", tri_depense.as_view(), name="tri_depense"),
    
    path("ajax_depense_projet/<int:projet_id>", ajax_depense_projet, name="ajax_depense_projet"),
    path("autre_type_depense/<str:type_depense>", autre_type_depense.as_view(), name="autre_type_depense"),
    path("ajax_devise/<int:projet_id>", ajax_devise, name="ajax_devise")

]