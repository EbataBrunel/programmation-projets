from django.urls import path
from .views import *

urlpatterns = [
    
    path('mp/<str:param>', mon_portfolio, name='mon_portfolio'),
    path('portfolio', portfolio, name='portfolio'),
    path('list-portfolio', list_portfolio, name='list_portfolio'),
    path("contact_portfolio", contact_portfolio, name="contact_portfolio"),
    
    path('projets', projects, name='projet/projects'),
    path("add-project", add_project, name="projet/add_project"),
    path("edit-projet/<str:id>", edit_project, name="projet/edit_project"),
    path("edit-proj", edit_proj, name="edit_proj"),
    path("del-projet/<str:id>", del_project, name="del_project"),
    
    path('theses', theses, name='these/theses'),
    path("add-these", add_these, name="these/add_these"),
    path("edit-these/<str:id>", edit_these, name="these/edit_these"),
    path("edit-th", edit_th, name="edit_th"),
    path("del-these/<str:id>", del_these, name="del_these"),
    
    path('these_article', these_article, name='article/these_article'),
    path("articles/<str:id>", articles, name="article/articles"),
    path("detail-article/<str:id>", detail_article, name="article/detail_article"),
    path("add-article", add_article, name="article/add_article"),
    path("edit-article/<str:id>", edit_article, name="article/edit_article"),
    path("edit-art", edit_art, name="edit_art"),
    path("del-article/<str:article_id>", del_article, name="del_article"),
    
    path("contact-pf", contact_pf, name="contact_pf"),
    path("del_contact/<int:id>", delete_contact, name="delete_contact")

]
