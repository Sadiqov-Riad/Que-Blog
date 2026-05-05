from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "cover_image", "category", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter a catchy title..."}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10, "placeholder": "Write your article here..."}),
            "cover_image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
