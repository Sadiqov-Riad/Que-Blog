from django.shortcuts import render


def post_list(request):
    return render(request, "posts/list.html")


def post_detail(request, post_id):
    return render(request, "posts/detail.html", {"post_id": post_id})


def post_create(request):
    return render(request, "posts/create.html")


def post_edit(request, post_id):
    return render(request, "posts/edit.html", {"post_id": post_id})
