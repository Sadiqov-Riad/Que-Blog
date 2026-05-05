from django.conf import settings
from django.db import models


class Reaction(models.Model):
    TYPE_LIKE = "like"
    TYPE_DISLIKE = "dislike"
    TYPE_HEART = "heart"
    TYPE_FIRE = "fire"
    TYPE_CHOICES = [
        (TYPE_LIKE, "Like"),
        (TYPE_DISLIKE, "Dislike"),
        (TYPE_HEART, "Heart"),
        (TYPE_FIRE, "Fire"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions"
    )
    post = models.ForeignKey(
        "posts.Post", on_delete=models.CASCADE, related_name="reactions"
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.type} by {self.user_id}"

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ratings")
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.score} stars by {self.user} on {self.post}"

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks")
    post = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"Bookmark by {self.user} for {self.post}"
