from django.urls import path
from .views import*

urlpatterns=[
    path("resumes", resumes, name="resumes"),
    path("add_resume", add_resume, name="add_resume"),
    path("edit_resume/<str:id>", edit_resume, name="edit_resume"),
    path("edit_res", edit_res, name="edit_res"),
    path("del_resume/<str:id>", del_resume, name="del_resume"),
    path("ajax_delete_resume/<int:id>", ajax_delete_resume, name="ajax_delete_resume"),    
    path("resumes_su", resumes_su, name="resumes_su"),
    path("ajax_list_resume/<str:month>", ajax_list_resume, name="ajax_list_resume")
]