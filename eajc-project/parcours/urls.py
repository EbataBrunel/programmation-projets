from django.urls import path
from .views import*

urlpatterns=[
    path("parcours", parcours, name="parcours"),
    path("add-parcours", add_parcours, name="add_parcours"),
    path("edit-parcours/<str:id>", edit_parcours, name="edit_parcours"),
    path("edit-par", edit_par, name="edit_par"),
    path("ajax_delete_parcours/<int:id>", ajax_delete_parcours, name="ajax_delete_parcours"),  
    path("del-parcours/<str:id>", del_parcours, name="del_parcours"),
    path("statpar/<int:id>", statpar.as_view(), name="statpar"),
    path("fetchpar/<int:id>", fetchpar.as_view(), name="fetchpar"),
    path("status/<str:id>", status.as_view(), name="status"),

    path("ajaxAnnee/<int:id>", getAnnee.as_view(), name="ajaxAnnee"),
    path("edit-parcours/ajaxAnnee/<int:id>", getAnneeEdit.as_view(), name="ajaxAnnee"),
    path("niveau/<str:id>", niveau.as_view(), name="niveau"),
    path("edit-parcours/niveau/<str:id>", niveau.as_view(), name="niveau")

]