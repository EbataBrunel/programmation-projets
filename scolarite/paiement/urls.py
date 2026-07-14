from django.urls import path
from .views import*

urlpatterns=[
    path("payments", payments, name="payments"),
    path("students_payments/<int:salle_id>", students_payments, name="students_payments"),
    path("detail_payment/<int:salle_id>/<int:student_id>", detail_payment, name="detail_payment"),
    path("add_payment", add_payment, name="add_payment"),
    path("edit_payment/<int:id>", edit_payment, name="edit_payment"),
    path("edit_py", edit_py, name="edit_py"),
    path("del_payment/<int:id>", del_payment, name="del_payment"),
    
    
    path("autorisation/autorisation_payments", autorisation_payments, name="autorisation/autorisation_payments"),
    path("autorisation/detail_autorisation_payments/<int:salle_id>", detail_autorisation_payments, name="autorisation/detail_autorisation_payments"),
    path("autorisation/add_autorisation_payment", add_autorisation_payment, name="autorisation/add_autorisation_payment"),
    path("autorisation/edit_autorisation_payment/<int:id>", edit_autorisation_payment, name="autorisation/edit_autorisation_payment"),
    path("edit-ap", edit_ap, name="edit_ap"),
    path("del_autorisation_payment/<int:id>", del_autorisation_payment, name="del_autorisation_payment"),
    path("autorisation/detail_autorisation_payments/ajax_delete_autorisation_student/<int:id>", ajax_delete_autorisation_student, name="ajax_delete_autorisation_student"),
    
    path("autorisation_paye_salle/autorisation_payments_salle", autorisation_payments_salle, name="autorisation_paye_salle/autorisation_payments_salle"),
    path("autorisation_paye_salle/add_autorisation_payment_salle", add_autorisation_payment_salle, name="autorisation_paye_salle/add_autorisation_payment_salle"),
    path("autorisation_paye_salle/edit_autorisation_payment_salle/<int:id>", edit_autorisation_payment_salle, name="autorisation_paye_salle/edit_autorisation_payment_salle"),
    path("edit_aps", edit_aps, name="edit_aps"),
    path("del-autorisation_payment_salle/<int:id>", del_autorisation_payment_salle, name="del_autorisation_payment_salle"),
    path("ajax_delete_autorisation_salle/<int:id>", ajax_delete_autorisation_salle, name="ajax_delete_autorisation_salle"),
    
    path("ajax_student_inscris/<int:id>", get_student_inscris_salle.as_view(), name="ajax_student_inscris"),
    path("edit-payment/ajax_student_inscris/<int:id>", get_student_inscris_salle.as_view(), name="ajax_student_inscris"),
    
    path("comptabilite_payment", comptabilite_payment, name="comptabilite_payment"),
    path("dossier-financier", dossier_financier, name="dossier_financier"),
    path("dossier-financier-parent", dossier_financier_parent, name="dossier_financier_parent"),
    
    path("recu-paye/<int:id>", recu_paye, name="recu_paye"),
    path("echeancier/<int:student_id>", echeancier, name="echeancier"),
    path("status_paye_parent/<int:student_id>", status_paye_parent, name="status_paye_parent"),
    path("dette_parents", dette_parents, name="dette_parents"),
    
    path("add_notification/<int:parent_id>/<str:montant>", add_notification, name="add_notification"),
    path("notification_parent", notification_parent, name="notification_parent")
]