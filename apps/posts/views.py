from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import PostForm
from .models import Post


def post_list(request):
    from django.core.paginator import Paginator
    from django.db.models import Count, Q, Avg, Exists, OuterRef
    from apps.reactions.models import Bookmark
    
    q = request.GET.get("q", "")
    
    posts_query = Post.objects.filter(status=Post.STATUS_PUBLISHED).select_related("author", "category").prefetch_related("tags")
    
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(post=OuterRef('pk'), user=request.user)
        posts_query = posts_query.annotate(is_bookmarked=Exists(bookmarks))
    
    posts_query = posts_query.annotate(
        avg_rating=Avg('ratings__score'),
        rating_count=Count('ratings', distinct=True)
    ).order_by("-published_at", "-created_at")
    
    if q:
        posts_query = posts_query.filter(Q(title__icontains=q) | Q(content__icontains=q))
    
    paginator = Paginator(posts_query, 5)  # Show 5 posts per page
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    return render(request, "posts/list.html", {"posts": posts, "q": q})


def post_detail(request, post_id):
    from django.db.models import Count, Avg, Exists, OuterRef
    from apps.reactions.models import Bookmark
    
    posts_query = Post.objects.select_related("author", "category").prefetch_related("tags")
    
    if request.user.is_authenticated:
        bookmarks = Bookmark.objects.filter(post=OuterRef('pk'), user=request.user)
        posts_query = posts_query.annotate(is_bookmarked=Exists(bookmarks))
        
    posts_query = posts_query.annotate(
        avg_rating=Avg('ratings__score'),
        rating_count=Count('ratings', distinct=True)
    )
    
    post = get_object_or_404(posts_query, pk=post_id, status=Post.STATUS_PUBLISHED)
    
    # Increment views count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    return render(request, "posts/detail.html", {"post": post})

@login_required
def pending_posts(request):
    if request.user.role not in ['admin', 'superadmin']:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
        
    posts = Post.objects.filter(status=Post.STATUS_PENDING).order_by("created_at")
    return render(request, "posts/pending.html", {"posts": posts})

@login_required
def approve_post(request, post_id):
    if request.user.role not in ['admin', 'superadmin']:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
        
    post = get_object_or_404(Post, pk=post_id, status=Post.STATUS_PENDING)
    post.status = Post.STATUS_PUBLISHED
    post.published_at = timezone.now()
    post.save()
    return redirect("posts:pending")


def process_tags_in_post_data(request):
    data = request.POST.copy()
    tags_list = data.getlist("tags")
    
    if not tags_list:
        return data

    from apps.categories.models import Tag
    from django.utils.text import slugify

    # The tags could be a single comma-separated string if it comes from an input field
    # or multiple strings if it comes from a select multiple.
    all_tags = []
    for val in tags_list:
        all_tags.extend([t.strip() for t in val.split(",") if t.strip()])

    new_tags_list = []
    for tag_name in all_tags:
        if tag_name.isdigit():
            # It might be an ID of an existing tag if submitted directly
            new_tags_list.append(tag_name)
        else:
            # It's a text tag
            slug = slugify(tag_name)
            if not slug:
                slug = "tag"
            
            # Ensure slug uniqueness if necessary by looking up by name first
            tag, created = Tag.objects.get_or_create(name=tag_name[:50], defaults={"slug": slug[:60]})
            new_tags_list.append(str(tag.id))
            
    data.setlist("tags", new_tags_list)
    return data

@login_required
def post_create(request):
    if request.method == "POST":
        data = process_tags_in_post_data(request)
        form = PostForm(data, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.user.role in ['admin', 'superadmin']:
                post.status = Post.STATUS_PUBLISHED
                post.published_at = timezone.now()
            else:
                post.status = Post.STATUS_PENDING
            post.save()
            form.save_m2m()
            return redirect("posts:detail", post_id=post.id)
    else:
        form = PostForm()

    return render(request, "posts/create.html", {"form": form})

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user and request.user.role not in ['admin', 'superadmin']:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    if request.method == "POST":
        data = process_tags_in_post_data(request)
        form = PostForm(data, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # If a regular user edits a post, it must go back to pending review
            if request.user.role not in ['admin', 'superadmin']:
                post.status = Post.STATUS_PENDING
            post.save()
            form.save_m2m()
            return redirect("posts:detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, "posts/edit.html", {"form": form, "post": post})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user and request.user.role not in ['admin', 'superadmin']:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied

    if request.method == "POST":
        post.delete()
        return redirect("posts:list")
    
    return render(request, "posts/delete.html", {"post": post})
