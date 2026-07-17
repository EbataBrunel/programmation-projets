from django.urls import path
from .views import *

urlpatterns = [
    
    path('contratremboursement/contrats_remboursements', contrats_remboursements, name='contratremboursement/contrats_remboursements'),
    path("contratremboursement/add_contrat_remboursement", add_contrat_remboursement, name="contratremboursement/add_contrat_remboursement"),
    path("contratremboursement/edit_contrat_remboursement/<str:id>", edit_contrat_remboursement, name="contratremboursement/edit_contrat_remboursement"),
    path("edit-cr", edit_cr, name="edit_cr"),
    path("del_contrat_remboursement/<str:id>", del_contrat_remboursement, name="del_contrat_remboursement"),
    
    path('remboursement/remboursements', remboursements, name='remboursement/remboursements'),
    path("remboursement/add_remboursement", add_remboursement, name="remboursement/add_remboursement"),
    path("remboursement/edit_remboursement/<str:id>", edit_remboursement, name="remboursement/edit_remboursement"),
    path("edit_remb", edit_remb, name="edit_remb"),
    path("del_remboursement/<str:id>", del_remboursement, name="del_remboursement"),
    
    path("ajax_contrat_remboursement/<int:contrat_id>", ajax_contrat_remboursement, name="ajax_contrat_remboursement"),
    path("ajax_devise/<int:projet_id>", ajax_devise, name="ajax_devise"),
    path("update_statut_remboursement", update_statut_remboursement, name="update_statut_remboursement"),
    
    path("add_signature", add_signature, name="add_signature"),
    path("document_signature-contrat/<int:contrat_id>", document_signature_contrat, name="document_signature_contrat"),
    path("document_decharge-remboursement/<str:remboursement_id>", document_decharge_remboursement, name="document_decharge_remboursement")
    
]

        

