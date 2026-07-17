from django.urls import path
from .views import*

urlpatterns=[

    path("annees", annees, name="annees"),
    path("add-annee", add_annee, name="add_annee"),
    path("edit-annee/<str:id>", edit_annee, name="edit_annee"),
    path("edit-an", edit_an, name="edit_an"),
    path("ajax_delete_annee/<int:id>", ajax_delete_annee, name="ajax_delete_annee"),  
    path("del-annee/<str:id>", del_annee, name="del_annee")

]



