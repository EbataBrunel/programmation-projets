from django.urls import path
from .views import *

urlpatterns = [
    
    # Progrès du proget personnel
    path('progres_p', progres_p, name='progres_p'),
    path("add_prog_p", add_prog_p, name="add_prog_p"),
    path("edit_prog_p/<str:id>", edit_prog_p, name="edit_prog_p"),
    path("edit_pro_p", edit_pro_p, name="edit_pro_p"),
    path("del_prog_p/<str:id>", del_prog_p, name="del_prog_p"),
    # Progrès du projet en commun
    path('progres_g', progres_g, name='progres_g'),
    path("add_prog_g", add_prog_g, name="add_prog_g"),
    path("edit_prog_g/<str:id>", edit_prog_g, name="edit_prog_g"),
    path("edit_pro_g", edit_pro_g, name="edit_pro_g"),
    path("del_prog_g/<str:id>", del_prog_g, name="del_prog_g"),
    
    path("tri_progres/<str:action>", tri_progres.as_view(), name="tri_progres"),
    
]
