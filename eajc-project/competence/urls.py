from django.urls import path
from .views import*

urlpatterns=[

    path("competences", competences, name="competences"),
    path("details-comp/<str:id>", details_comp, name="details_comp"),
    path("add-comp", add_comp, name="add_comp"),
    path("edit-comp/<str:id>", edit_comp, name="edit_comp"),
    path("edit-comp/ajaxcomp/<int:id>", ajaxcomp.as_view(), name="ajaxcomp"),
    path("edit-cmp", edit_cmp, name="edit_cmp"),
    path("ajax_delete_multiple_competence/<int:id>", ajax_delete_multiple_competence, name="ajax_delete_multiple_competence"),
    path("delete-comp/<str:id>", delete_comp, name="delete_comp"),
    path("details-comp/ajax_delete_competence/<int:id>", ajax_delete_competence, name="ajax_delete_competence"), 
    path("del-comp/<str:id>", del_comp, name="del_comp"),
    path("details-comp/statcomp/<int:id>", statcomp.as_view(), name="statcomp"),
    path("fetchcomp/<str:id>", fetchcomp.as_view(), name="fetchcomp"),
    path("ajaxcomp/<int:id>", ajaxcomp.as_view(), name="ajaxcomp"),
    
    
    path("type-competences", type_competences, name="typeCompetence/type_competences"),
    path("add-type-competence", add_type_competence, name="typeCompetence/add_typeCompetence"),
    path("edit-type-competence/<str:id>", edit_type_competence, name="typeCompetence/edit_typeCompetence"),
    path("edit-typec", edit_typec, name="edit_typec"),
    path("ajax_delete_type_competence/<int:id>", ajax_delete_type_competence, name="ajax_delete_type_competence"),  
    path("del_type_competence/<str:id>", del_type_competence, name="del_type_competence")  

]


