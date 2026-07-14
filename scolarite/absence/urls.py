from django.urls import path
from .views import*

urlpatterns=[
    path("absences", absences, name="absences"),
    path("detail_salle_absence/<int:enseignant_id>", detail_salle_absence, name="detail_salle_absence"),
    path("detail_absences/<int:enseignant_id>/<int:salle_id>", detail_absences, name="detail_absences"),
    path("save_absence/<int:emploi_id>", save_absence, name="save_absence"),
    path("save_ab", save_ab, name="save_ab"),
    path("edit_absence/<int:id>", edit_absence, name="edit_absence"),
    path("edit_ab/", edit_ab, name="edit_ab"),
    path("del_absence/<int:id>", del_absence, name="del_absence"),
    path("mes_absences", mes_absences, name="mes_absences"),
    path("mes_absences_admin", mes_absences_admin, name="mes_absences_admin"),
    
    path("presence_student/<int:id>", presence_student, name="presence_student"),
    path("abs_students", abs_students, name="abs_students"),
    path("abs_student_user", abs_student_user, name="abs_student_user"),
    path("abs_student_mat_user/<int:student_id>", abs_student_mat_user, name="abs_student_mat_user"),
    path("presence-student/save_absencestudent/<int:id>/<int:emargement_id>", save_absencestudent.as_view(), name="save_absencestudent"),
    path("abs_studentmatiere/<int:salle_id>/<int:matiere_id>", abs_studentmatiere, name="abs_studentmatiere"),
    
    
    path("absences_admin", absences_admin, name="absences_admin"),
    path("add_absence_admin", add_absence_admin, name="add_absence_admin"),
    path("edit_absence_admin/<int:id>", edit_absence_admin, name="edit_absence_admin"),
    path("edit_aa", edit_aa, name="edit_aa"),
    path("del_absence_admin/<int:id>", del_absence_admin, name="del_absence_admin"),
    path("ajax_delete_absence_admin/<int:id>", ajax_delete_absence_admin, name="ajax_delete_absence_admin"),

]