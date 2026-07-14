from django.urls import path, reverse_lazy
from .views import*
from django.contrib.auth import views as auth_views
#from django.contrib.auth import views as auth_views

urlpatterns=[
    path("add_annee_setting", add_annee_setting, name="add_annee_setting" ),
    path("register", register, name="user/register"),
    path("success-account/<int:id>", success_account, name="user/success-account"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
    path("login", login_user, name="connection/login"),
    path("logout", logout_user, name="logout"),
    path("connexion", login_customer, name="connection/connexion"),
    path("logout_customer", logout_customer, name="logout_customer"),
    
    path("user/admin/", administrator, name="user/admin"),
    path("user/detail_admin/<int:id>", detail_admin, name="user/detail_admin"),
    path("del_admin/<int:id>", del_admin, name="del_admin"), 
    path("user/delete_admin/<int:id>", delete_admin, name="user/delete_admin"),    
    path("teacher/teachers/", teachers, name="teacher/teachers"),    
    path("teacher/detail_teacher/<int:id>", detail_teacher, name="teacher/detail_teacher"),
    path("teacher/delete-teacher/<int:id>", delete_teacher, name="teacher/delete_teacher"),
    path("del-teacher/<int:id>", del_teacher, name="del_teacher"),  
    path("user/profile/", profile, name="user/profile"),
    path("profile_sup_admin/", profile_sup_admin, name="user/profile_sup_admin"),
    path("edit_profile_photo", edit_profile_photo, name="edit_profile_photo"),
    path("user/permission/<int:user_id>", permission, name="user/permission"),
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
    # Gestion des parents
    path("parent/parents", parents, name="parent/parents"),
    path("parent/detail_parent/<int:id>", detail_parent, name="parent/detail_parent"),
    path("parent/parent_parent/profil_parent", profile_parent, name="parent/profile_parent"),
    path("parent/add_parent", add_parent, name="parent/add_parent"),
    path("parent/edit_parent/<int:id>", edit_parent, name="parent/edit_parent"),
    path("edit_pa", edit_pa, name="edit_pa"),
    path("del_parent/<int:id>", del_parent, name="del_parent"),
    path("parent/delete_parent/<int:id>", delete_parent, name="parent/delete_parent"),
    path("update_password_parent", update_password_parent, name="update_password_parent"),
    # Gestion des étudiants
    path("student/students", students, name="student/students"),
    path("student/detail_student/<int:id>", detail_student, name="student/detail_student"),
    path("student/profil_student", profile_student, name="student/profile_student"),
    path("student/add_student", add_student, name="student/add_student"),
    path("student/edit_student/<int:id>", edit_student, name="student/edit_student"),
    path("edit_st", edit_st, name="edit_st"),
    path("del_student/<int:id>", del_student, name="del_student"),
    path("update_password", update_password, name="update_password"),
    
    
    path("group/groups", groupes, name="group/groups"),
    path("group/add_group", add_group, name="group/add_group"),
    path("group/edit_group/<int:id>", edit_group, name="group/edit_group"),
    path("edit_gr", edit_gr, name="edit_gr"),
    path("del_group/<int:id>", del_group, name="del_group"),

    path("group/admin_group/<int:id>", admin_group, name="group/admin_group"),
    path("add_admin_to_group", add_admin_to_group, name="add_admin_to_group"),
    path("del_user_to_group/<int:id>/<str:name>", del_user_to_group, name="del_user_to_group"),
]