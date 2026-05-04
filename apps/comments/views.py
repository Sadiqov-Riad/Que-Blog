from django.shortcuts import render


def comment_preview(request):
    return render(request, "comments/_comment.html")
