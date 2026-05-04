from django.shortcuts import render


def category_list(request):
    return render(request, "categories/list.html")
