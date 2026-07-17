from django.urls import path
from .views import *

urlpatterns = [
 
    path('devises', devises, name='devises'),
    path("add_devise", add_devise, name="add_devise"),
    path("edit_devise/<str:id>", edit_devise, name="edit_devise"),
    path("edit_dev", edit_dev, name="edit_dev"),
    path("ajax_delete_devise/<int:id>", ajax_delete_devise, name="ajax_delete_devise"),
    path("del_devise/<str:id>", del_devise, name="del_devise"),
    
]
