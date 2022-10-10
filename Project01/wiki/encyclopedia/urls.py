from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("createNewPage", views.newPage, name="createNewPage"),
    path("edit", views.edit, name="edit"),
    path("random", views.randomPage, name="random"),
    path("<str:title>", views.entry, name="entry"),    
]

# path("<str:title>", views.entry, name="entry") les URLS avec str: doivent toujours être dernière de la liste