from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import*
from .forms import*

urlpatterns=[
    path("register", register, name="users/register"),
    path("success-account/<int:id>", success_account, name="users/success-account"),
    path("login", login_user, name="connection/login"),
    path("connexion", login_customer, name="connection/connexion"),
    path("logout", logout_user, name="logout"),
    path("users", users, name="users/users"),
    path("ajax_delete_user/<int:id>", ajax_delete_user, name="ajax_delete_user"),  
    path("del-user/<str:id>", del_user, name="del_user"),
    path("m-countries", m_countries, name="users/m-countries"),
    path("detail-user/<str:id>", detail_user, name="users/detail_user"),
    path("delaccount-user/<int:id>", delaccount_user, name="delaccount_user"),

    path("customers", customers, name="users/customers"),
    path("ajax_delete_customer/<int:id>", ajax_delete_customer, name="ajax_delete_customer"), 
    path("del-customer/<str:id>", del_customer, name="del_customer"), 
    path("details-cus/<str:id>", details_cus, name="users/details_cus"),
    path("members", members, name="users/members"),

    path('upd-access/<int:id>', upd_access, name='users/upd_access'),
    path("profil", profile, name="users/profile"),
    path("edit-profile", edit_profile, name="users/edit_profile"),
    path("demandeDeleteAccount", demande_delete_account, name="demandeDeleteAccount"),
    path("answer-del-account/<int:id>", answer_del_account, name="users/answer_del_account"),
    path("answerDeleteAccount", answer_delete_account, name="answerDeleteAccount"),
    path("parametre", param, name="parametre"),
    path("configuration", configuration, name="users/configuration"),
    path("priority/<int:id>", priority.as_view(), name="priority"),
    path("useraskdeleteaccount", user_dmd_delete_account, name="users/useraskdeleteaccount"),
    
    path("groups", groupes, name="group/groups"),
    path("ajax_delete_group/<int:id>", ajax_delete_group, name="ajax_delete_group"),
    path("del-group/<str:id>", del_group, name="del_group"),

    path("add-guser/<int:id>", add_user_group, name="users/add_user_group"),
    path("add-ug/", add_ug, name="users/add_ug"),
    path("user-group/<str:id>", user_groups, name="users/user_groups"),
    path("user-group/ajax_delete_user_group/<int:id>/<str:name>", ajax_delete_user_group, name="ajax_delete_user_group"),
    path("add_user_to_group", add_user_to_group, name="add_user_to_group"),
    path("del_user_to_group/<str:id>/<str:name>", del_user_to_group, name="del_user_to_group"),

    path("password_change", 
         auth_views.PasswordChangeView.as_view(
            template_name="password/change-password.html", 
            success_url=reverse_lazy('password_change_done'),
            form_class=PasswordChangingForm
        ), 
        name="password/password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="password/password_change_success.html"), name="password_change_done"),

    path("reset_password", auth_views.PasswordResetView.as_view(
            template_name="password/password_reset.html",
            success_url=reverse_lazy('password_reset_done'),
            form_class=PasswordResForm
        ), 
        name="reset_password"),
    
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(
        template_name="password/password_reset_sent.html"), 
         name="password_reset_done"),
    
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
            template_name="password/password_reset_form.html",
        ), 
        name="password_reset_confirm"),
    path("reset_password_complet", auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), name="password_reset_complete"),
    
    path("activate/<uidb64>/<token>", activate, name="activate")
]


#Mix - Dennis Ivy