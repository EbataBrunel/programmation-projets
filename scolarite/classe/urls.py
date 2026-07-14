from django.urls import path
from .views import*
#from django.contrib.auth import views as auth_views

urlpatterns=[
    path("classes/", classes, name="classes"),
    path("add_class/", add_class, name="add_class"),
    path("edit_class/<int:id>", edit_class, name="edit_class"),
    path("edit_cl/", edit_cl, name="edit_cl"),
    path("del_class/<int:id>", del_class, name="del_class"),
    path("delete_classe/<int:id>", delete_classe, name="delete_classe")
]