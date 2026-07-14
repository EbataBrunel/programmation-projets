from django.urls import path
from .views import*
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path("settings/setting", setting, name="settings/setting"),
    path("settings/setting_supuser", setting_supuser, name="settings/setting_supuser"),
    path("settings/maintenance", maintenance, name="settings/maintenance"),
    path("settings/authorization", authorization, name="settings/authorization"),
    path("settings/dashboard/<int:id>", dashboard, name="settings/dashboard"),
    path("settings/db_classe/<int:id>", db_classe, name="settings/db_classe"),
    path("settings/db", db, name="settings/db"),
    path("settings/home", home, name="settings/home"),
    path("settings/resources_admin", resources_admin, name="settings/resources_admin"),
    path("settings/resources_admin_parent", resources_admin_parent, name="settings/resources_admin_parent"),
    path("settings/resources_admin_user", resources_admin_user, name="settings/resources_admin_user"),
    path("settings/help", need_help, name="settings/help"),
    path("ajaxyear/<int:id>", ajaxyear.as_view(), name="ajaxyear"),
    path("settings/fetchgroup/<int:id>", fetchgroup.as_view(), name="fetchgroup"),
    path("ajax_group_name/<str:group_name>", ajax_group_name.as_view(), name="ajax_group_name"),
    
    path("send_message", send_message, name="send_message")
]