from django.urls import path
from .views import*

urlpatterns=[
    path("emargements", emargements, name="emargements"),
    path("salles_emargements/<int:enseignant_id>", salles_emargements, name="salles_emargements"),
    path("matieres_emargements/<int:enseignant_id>/<int:salle_id>", matieres_emargements, name="matieres_emargements"),
    path("months_emargements/<int:enseignant_id>/<int:salle_id>/<int:matiere_id>", months_emargements, name="months_emargements"),
    path("detail_emargements/<int:enseignant_id>/<int:salle_id>/<int:matiere_id>/<str:month>", detail_emargements, name="detail_emargements"),
    path("add_emargement/<int:emploi_id>", add_emargement, name="add_emargement"),
    path("add_em", add_em, name="add_em"),
    path("edit_emargement/<int:id>", edit_emargement, name="edit_emargement"),
    path("edit_em", edit_em, name="edit_em"),
    path("del_emargement/<int:id>", del_emargement, name="del_emargement"),
    
    path("mes_emargements", mes_emargements, name="mes_emargements"),
    path("heures_emargements", heures_emargements, name="heures_emargements"),
    path("ajax_heures_emargements/<str:month>", ajax_heures_emargements, name="ajax_heures_emargements"),
    path("ajax_emargements_ens/<str:month>", ajax_emargements_ens, name="ajax_emargements_ens"),
]