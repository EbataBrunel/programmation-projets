from django.urls import path
from .views import*

urlpatterns=[
    path("annonces", annonces, name="annonce/annonces"),
    path("annonce", annonce, name="annonce/annonce"),
    path("mes-annonce", mes_annonce, name="annonce/mes-annonce"),
    path("ajax_detail_annonce/<int:id>", ajax_detail_annonce, name="ajax_detail_annonce"), 
    path("add-annonce", add_annonce, name="annonce/add-annonce"),
    path("edit-annonce/<str:id>", edit_annonce, name="annonce/edit-annonce"),
    path("ajax_delete_annonce/<int:id>", ajax_delete_annonce, name="ajax_delete_annonce"),  
    path("del-annonce/<str:id>", del_annonce, name="del-annonce"),
    path("ajax_delete_my_ad/<int:id>", ajax_delete_my_ad, name="ajax_delete_my_ad"), 
    path("delete-my-ad/<str:id>", delete_my_ad, name="delete-my-ad"),
    path("delete-annonce/<str:id>", delete_annonce, name="delete-annonce"),
    path("ajax_visibilite_annonce/<int:id>", ajax_visibilite_annonce, name="ajax_visibilite_annonce"),
    path("visibility/<int:id>", visibilite, name="visibility") 
]