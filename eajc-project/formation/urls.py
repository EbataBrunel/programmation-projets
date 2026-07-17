from django.urls import path
from .views import*

urlpatterns=[
    
    path("formations", formations, name="formations"),
    path("add-form", add_form, name="add_form"),
    path("edit-form/<str:id>", edit_form, name="edit_form"),
    path("edit-for", edit_for, name="edit_for"),
    path("ajax_delete_form/<int:id>", ajax_delete_form, name="ajax_delete_form"),  
    path("del-form/<str:id>", del_form, name="del_form")

]
