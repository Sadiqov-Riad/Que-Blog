from django.urls import path

from . import views

app_name = "comments"

urlpatterns = [
    path("preview/", views.comment_preview, name="preview"),
]
