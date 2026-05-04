from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.posts.urls")),
    path("users/", include("apps.users.urls")),
    path("categories/", include("apps.categories.urls")),
    path("comments/", include("apps.comments.urls")),
    path("reactions/", include("apps.reactions.urls")),
    path("subscriptions/", include("apps.subscriptions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
