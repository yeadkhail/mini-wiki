from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.title,name="title"),
    path("new",views.new,name="new"),
    path("edit/<str:name>",views.edit,name="edit"),
    path("random",views.randcontent,name="randcontent"),
]
