from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("list/", views.user_list_view, name="user_list"),
    path("ban/<int:user_id>/", views.ban_user_view, name="ban_user"),
    path("unban/<int:user_id>/", views.unban_user_view, name="unban_user"),
    path("change-role/<int:user_id>/<str:new_role>/", views.change_role_view, name="change_role"),
]
