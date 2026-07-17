from django.urls import path
from .views import*

#Lien pour la fusion des fichiers
#https://www.youtube.com/watch?v=4gZgWXJpX-w 
urlpatterns=[
    path("lms", lms, name="lms"),
    path("del-lm/<str:id>", del_lm, name="del_lm"),
    path("delete-lm/<str:id>", delete_lm, name="delete_lm"),
    path("edit-lm/<str:id>", edit_lm, name="edit_lm"),
    path("edit-l", edit_l, name="edit_l"),

    path("all-lms", all_lms, name="all_lms"),
    path("cv-lm", cv_lm, name="cv_lm"),
    path("p-lms", p_lms, name="p_lms"),
    
    path("valid-lm/<int:id>", valid_lm, name="valid_lm"),
    path("valid-lm/ajaxlm/<int:id>", ajaxlm.as_view(), name="ajaxlm"),
]