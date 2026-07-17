from django.urls import path
from .views import*

urlpatterns=[

    path("experiences", experiences, name="experiences"),
    path("ajax_detail_experience/<int:id>", ajax_detail_experience, name="ajax_detail_experience"),
    path("add-exp", add_exp, name="add_exp"),
    path("ajax_delete_experience/<int:id>", ajax_delete_experience, name="ajax_detail_experience"),  
    path("del-exp/<str:id>", del_exp, name="del_exp"),
    path("edit-exp/<str:id>", edit_exp, name="edit_exp"),
    path("edit-ex", edit_ex, name="edit_ex"),
    path("statexp/<int:id>", statexp.as_view(), name="statexp"),

    path("ajax/<str:id>", getFormExperience.as_view(), name="ajax"),
    path("ajaxdate/<str:id>", getFormExperienceDate.as_view(), name="ajaxdate"),
    path("edit-exp/ajax/<str:id>/<int:code>", getFormExperienceEdit.as_view(), name="ajax"),
    path("edit-exp/ajaxdate/<str:id>/<int:code>", getFormExperienceEditDate.as_view(), name="ajaxdate"),
]
