from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Category
from apps.posts.models import Post

def category_list(request):
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status=Post.STATUS_PUBLISHED))
    ).order_by('-post_count', 'name')
    return render(request, "categories/list.html", {"categories": categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    
    posts_query = (
        Post.objects.filter(category=category, status=Post.STATUS_PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
        .annotate(
            likes=Count("reactions", filter=Q(reactions__type="like")),
            dislikes=Count("reactions", filter=Q(reactions__type="dislike")),
        )
        .order_by("-published_at", "-created_at")
    )
    
    paginator = Paginator(posts_query, 5)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    return render(request, "categories/detail.html", {"category": category, "posts": posts})
