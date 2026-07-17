from django.urls import path
from .views import*
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path("setting", setting, name="settings/setting"),
    path("maitenance", maintenance, name="settings/maintenance"),
    path("update_satus_project_and_task", update_satus_project_and_task, name="update_satus_project_and_task"),
    
]