from django.urls import path
from .views import*

urlpatterns=[

    path("entreprises", entreprises, name="entreprises"),
    path("add-ent", add_ent, name="add_ent"),
    path("edit-ent/<str:id>", edit_ent, name="edit_ent"),
    path("edit-ent", edit_en, name="edit_en"),
    path("ajax_delete_entreprise/<int:id>", ajax_delete_entreprise, name="ajax_delete_entreprise"),  
    path("del-ent/<str:id>", del_ent, name="del_ent")

]


