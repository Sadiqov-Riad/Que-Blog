from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("create/", views.post_create, name="create"),
    path("<int:post_id>/", views.post_detail, name="detail"),
    path("<int:post_id>/edit/", views.post_edit, name="edit"),
]
