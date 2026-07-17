from django.urls import path
from .views import*
from django.conf.urls import handler404, handler500

urlpatterns=[
    path("etablissements", etablissements, name="etablissements"),
    path("add-etab", add_etab, name="add_etab"),
    path("edit-etab/<str:id>", edit_etab, name="edit_etab"),
    path("edit-eta", edit_eta, name="edit_eta"),
    path("ajax_delete_etab/<int:id>", ajax_delete_etab, name="ajax_delete_etab"),  
    path("del-etab/<str:id>", del_etab, name="del_etab")
]


