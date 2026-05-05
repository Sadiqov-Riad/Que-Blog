from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Reaction
from apps.posts.models import Post


@login_required
@require_POST
def reaction_toggle(request):
    post_id = request.POST.get("post_id")
    reaction_type = request.POST.get("reaction_type")

    valid_types = {choice[0] for choice in Reaction.TYPE_CHOICES}
    if reaction_type not in valid_types:
        return redirect(request.POST.get("next") or "/")

    post = get_object_or_404(Post, pk=post_id)
    existing = Reaction.objects.filter(user=request.user, post=post).first()

    if existing and existing.type == reaction_type:
        existing.delete()
    elif existing:
        existing.type = reaction_type
        existing.save(update_fields=["type"])
    else:
        Reaction.objects.create(user=request.user, post=post, type=reaction_type)

    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)
@login_required
@require_POST
def bookmark_toggle(request):
    post_id = request.POST.get("post_id")
    post = get_object_or_404(Post, pk=post_id)
    
    from .models import Bookmark
    bookmark = Bookmark.objects.filter(user=request.user, post=post).first()
    
    if bookmark:
        bookmark.delete()
    else:
        Bookmark.objects.create(user=request.user, post=post)
        
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)

@login_required
@require_POST
def set_rating(request):
    post_id = request.POST.get("post_id")
    score = int(request.POST.get("score", 0))
    post = get_object_or_404(Post, pk=post_id)
    
    if 1 <= score <= 5:
        from .models import Rating
        rating, created = Rating.objects.update_or_create(
            user=request.user, post=post,
            defaults={"score": score}
        )
        
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)
