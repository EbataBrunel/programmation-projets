from django.urls import path, reverse_lazy
from .views import*
from django.contrib.auth import views as auth_views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register", register, name="user/register"),
    path("success-account/<int:id>", success_account, name="user/success-account"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("login", login_user, name="connection/login"),
    path("logout", logout_user, name="logout"),
    
    path("user/users/", users, name="user/users"),
    path("user/users/ajax_detail_user/<int:id>", ajax_detail_user, name="ajax_detail_user"),
    path("profile/", profile, name="user/profile"),
    path("user/edit_profile/", edit_profile, name="user/edit_profile"),
    path("user/users/ajax_delete_user/<int:id>", ajax_delete_user, name="ajax_delete_user"),  
    path("del_user/<str:id>", delete_user, name="del_user"),
    path("user/permission/<str:user_id>", permission, name="user/permission"),
    path("upadate_permission", update_permission, name="update_permission"),
    path("permission/ajax_active_permission/<str:actif>", ajax_active_permission, name="ajax_active_permission"),
    path("permission/ajax_staff_permission/<str:staff>", ajax_staff_permission, name="ajax_staff_permission"),
    path("permission/ajax_superuser_permission/<str:superuser>", ajax_superuser_permission, name="ajax_superuser_permission"),
    
    # Changer le mot de passe
    path("password_change", CustomPasswordChangeView.as_view(), name="password_change"),   
    path("password_change/done/", CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    # Réinitailisation du mot de passe
    path("reset_password", CustomPasswordResetView.as_view(), name="reset_password"),   
    path("reset_password_sent", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),   
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),    
    path("reset_password_complet", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]