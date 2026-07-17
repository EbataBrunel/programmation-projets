from django.urls import path
from .views import*
from django.conf.urls import handler404, handler500

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("fresh_header", fresh_header, name="fresh_header"),
    path("count_new_chat", count_new_chat, name="count_new_chat"),
    path("contact", contact, name="contact/contact"),
    path("contacts", contacts, name="contact/contacts"),
    path("del-contact/<int:id>", del_contact, name="contact/del_contact"),
    path("delete-contact/<int:id>", delete_contact, name="contact/delete_contact"),
    path("detmes/del_message/<int:id>", del_message.as_view(), name="del_message"),
    path("delete_messages/<int:id>", delete_messages, name="contact/delete_messages"),
    path("details-contact/<str:id>", details_contact, name="contact/details_contact"),
    path("contactuser/<str:id>", contactuser, name="contact/contactuser"),
    path("contuser", contuser, name="contact/contuser"),
    path("messages", messag, name="contact/messages"),
    path("detmes/<int:id>", detmes, name="contact/detmes"),
    path("apropos", apropos, name="contact/apropos"),
    path("services", services, name="contact/services"),

    path("maintenance", maintenance, name="maintenance"),
    path("statistique", statistique, name="statistique"),
    path("authorization", authorization, name="authorization"),
    path("step-cv", step_cv, name="cv/step_cv"),
    path("recap", recap, name="cv/recap"),
    path("recap-1", recap_1, name="cv/recap-1"),
    path("recap-2", recap_2, name="cv/recap-2"),
    path("profile-user/<str:id>", p_user, name="cv/profile_user"),
    path("profuser/<str:id>", profuser, name="cv/profuser"),
    path("generatecv-1", generatecv_1, name="cv/generatecv-1"),
    path("generatecv-2", generatecv_2, name="cv/generatecv-2"),
    path("gencv", gencv, name="cv/gencv")

]

handler404 = "eab.views.handler404"
handler500 = "eab.views.handler500"


