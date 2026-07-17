from django.urls import path
from .views import*

urlpatterns=[
    path("references", references, name="references"),
    path("add-ref", add_ref, name="add_ref"),
    path("ajax_delete_reference/<int:id>", ajax_delete_reference, name="ajax_delete_reference"),
    path("del-ref/<str:id>", del_ref, name="del_ref"),
    path("edit-ref/<str:id>", edit_ref, name="edit_ref"),
    path("edit-re", edit_re, name="edit_re"),
    path("statref/<int:id>", statref.as_view(), name="statref"),
]