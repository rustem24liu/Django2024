from django import forms
from django.forms import widgets

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        exclude = ['author']

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control mb-3 w-50', "placeholder": "Title"}),
            'body' : forms.Textarea(attrs={'class': 'form-control mb-3 w-50', "placeholder": "Your post ..."}),
            'author' : forms.Select(attrs={'class': 'form-select w-50', "placeholder": "Author"}),
            'image' : forms.FileInput(attrs={'class': 'form-control w-50', "placeholder": "Image"   }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control mb-3', "placeholder": "Your comment..."}),
        }
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='search')
