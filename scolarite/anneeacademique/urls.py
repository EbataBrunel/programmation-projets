from django.urls import path
from .views import*
#from django.contrib.auth import views as auth_views

urlpatterns=[
    path("annee_academiques", anneeacademiques, name="annee_academiques"),
    path("add_anneeacademique", add_anneeacademique, name="add_anneeacademique"),
    path("edit_anneeacademique/<int:id>", edit_anneeacademique, name="edit_anneeacademique"),
    path("edit-anneeac", edit_anneeac, name="edit_anneeac"),
    path("delete_anneeacademique/<int:id>", delete_anneeacademique, name="delete_anneeacademique"),
    path("del_anneeacademique/<int:id>", del_anneeacademique, name="del_anneeacademique"),
    path("cloture_anneeacademique/<int:id>", cloture_anneeacademique, name="cloture_anneeacademique"),
    path("clot_sanneeacademique", clot_anneeacademique, name="clot_anneeacademique")
]