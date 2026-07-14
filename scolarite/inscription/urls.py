from django.urls import path
from .views import *

urlpatterns=[
    path("inscriptions", inscriptions, name="inscriptions"),
    path("detail_inscription/<int:id>", detail_inscription, name="detail_inscription"),
    path("add_inscription", add_inscription, name="add_inscription"),
    path("edit_inscription/<int:id>", edit_inscription, name="edit_inscription"),
    path("edit_in", edit_in, name="edit_in"),
    path("del_inscription/<int:id>", del_inscription, name="del_inscription"),
    
    path("comptabilite_inscription", comptabilite_inscription, name="comptabilite_inscription"),
    path("inscriptions_enseignant", inscriptions_enseignant, name="inscriptions_enseignant"),
    path("inscriptions_admin", inscriptions_admin, name="inscriptions_admin"),
    path("attestation_inscription/<int:student_id>", attestation_inscription, name="attestation_inscription")
]