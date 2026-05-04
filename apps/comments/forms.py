from django import forms


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=150)
    body = forms.CharField(widget=forms.Textarea)
