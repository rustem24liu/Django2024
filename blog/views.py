from django.shortcuts import render
from urllib import request

from .models import Post


# Create your views here.
def index(request):
    return render(request, 'main-page/index.html')

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, 'main-page/posts.html', context={'posts': posts})
