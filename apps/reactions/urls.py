from django.urls import path

from . import views

app_name = "reactions"

urlpatterns = [
    path("toggle/", views.reaction_toggle, name="toggle"),
]
