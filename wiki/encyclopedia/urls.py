from django.urls import path

from . import views


app_name="encyclopedia"
urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("wiki/random_page", views.random_page, name="random_page"),
    path("wiki/search_page", views.search_page, name="search_page"),
    path("wiki/about", views.about, name="about"),
    path("wiki/<slug:title>", views.visit_entry, name="visit_entry"),
    path("wiki/edit/<str:pageName>", views.edit, name="edit"),
   
]
