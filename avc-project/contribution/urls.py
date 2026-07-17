from django.urls import path
from .views import *

urlpatterns = [
    
    # Projets personnels
    path('contributions', contributions, name='contributions'),
    path("add_contribution", add_contribution, name="add_contribution"),
    path("edit_contribution/<str:id>", edit_contribution, name="edit_contribution"),
    path("edit-con", edit_cont, name="edit_cont"),
    path("del-contribution/<str:id>", del_contribution, name="del_contribution"),
    path("ajax_actionnaire_contribution/<int:projet_id>", ajax_actionnaire_contribution, name="ajax_actionnaire_contribution"),
    path("ajax_devise/<int:projet_id>", ajax_devise, name="ajax_devise")

]
