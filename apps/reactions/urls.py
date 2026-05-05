from django.urls import path

from . import views

app_name = "reactions"

urlpatterns = [
    path("toggle/", views.reaction_toggle, name="toggle"),
    path("bookmark/", views.bookmark_toggle, name="bookmark_toggle"),
    path("rating/", views.set_rating, name="set_rating"),
]
