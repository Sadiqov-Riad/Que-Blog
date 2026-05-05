from django.conf import settings
from django.db import models


class Post(models.Model):
    STATUS_DRAFT = "draft"
    STATUS_PENDING = "pending"
    STATUS_PUBLISHED = "published"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PENDING, "Pending"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT
    )
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField("categories.Tag", blank=True, related_name="posts")

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = "post"
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def get_excerpt(self):
        import json
        from django.utils.html import strip_tags
        try:
            data = json.loads(self.content)
            if "blocks" in data:
                text_blocks = []
                for block in data["blocks"]:
                    if block["type"] in ["paragraph", "header", "list"]:
                        if block["type"] == "list" and "items" in block["data"]:
                            for item in block["data"]["items"]:
                                if isinstance(item, dict) and "content" in item:
                                    text_blocks.append(item["content"])
                                elif isinstance(item, str):
                                    text_blocks.append(item)
                        else:
                            text_blocks.append(block["data"].get("text", ""))
                
                full_text = " ".join(text_blocks)
                clean_text = strip_tags(full_text)
                words = clean_text.split()
                if len(words) > 30:
                    return " ".join(words[:30]) + "..."
                return clean_text
        except:
            pass
            
        clean = strip_tags(self.content)
        words = clean.split()
        if len(words) > 30:
            return " ".join(words[:30]) + "..."
        return clean

    def __str__(self):
        return self.title


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_views",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View for {self.post_id}"


class Draft(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="drafts")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="drafts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title
