from django.urls import path
from .views import*

urlpatterns=[
    path("emploitemps", emploitemps, name="emploitemps"),
    path("emploitemps_student", emploitemps_student, name="emploitemps_student"),
    path("emploitemps_parent", emploitemps_parent, name="emploitemps_parent"),
    path("add_emploitemps", add_emploitemps, name="add_emploitemps"),
    path("edit_emploitemps/<int:id>", edit_emploitemps, name="edit_emploitemps"),
    path("edit_emp", edit_emp, name="edit_emp"),
    path("del_emploitemps/<int:id>", del_emploitemps, name="del_emploitemps"),
    path("ajax_matiere/<int:id>", get_matiere_programmer_salle_emploi.as_view(), name="ajax_matiere"),
    path("emploitemps/ajax_matiere/<int:id>", get_matiere_programmer_salle_emploi.as_view(), name="ajax_matiere"),
    path("content_emploitemps/<int:id>", content_emploitemps.as_view(), name="content_emploitemps"),
    path("content_emploitemps_parent/<int:id>", content_emploitemps_parent.as_view(), name="content_emploitemps_parent")
]