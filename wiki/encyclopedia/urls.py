from django.urls import path
from . import views

app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("searchresults", views.searchresults, name="searchresults"),
    path("search", views.search, name="search"),
    path("random_page", views.randomPage, name="random_page")
]
