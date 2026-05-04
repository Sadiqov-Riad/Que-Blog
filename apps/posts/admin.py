from django.contrib import admin

from .models import Draft, Post, PostView

admin.site.register(Post)
admin.site.register(PostView)
admin.site.register(Draft)
