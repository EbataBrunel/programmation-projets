from django.urls import path
from .views import*

urlpatterns=[

    path("baccalaureat", baccalaureat, name="baccalaureat"),
    path("del-bac/<int:id>", delete_baccalaureat, name="del_bac"),
    path("diplome/<str:id>", diplome.as_view(), name="diplome")

]