from lib2to3.fixes.fix_input import context

from django.shortcuts import reverse, render, redirect, get_object_or_404
from django.shortcuts import render
from urllib import request

from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView


# Create your views here.
def index(request):
    return render(request, 'main-page/index.html')

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, 'main-page/post/posts.html', context={'posts': posts})

class PostListVies(ListView):
    template_name = "main-page/post/posts.html"
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostDetailView(DetailView):
    template_name = 'main-page/post/post-detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_form = CommentForm()
        post = self.object
        comments = post.comments.all()
        context['comment_form'] = comment_form
        context['comments'] = comments
        return context

class PostCreateView(CreateView):
    template_name = "main-page/post/create_post.html"
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

    def get_success_url(self):
        return reverse('post-list')

class PostUpdateView(UpdateView):
    template_name = "main-page/post/update-post.html"
    model = Post
    form_class = PostForm
    context_key = 'post'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

class PostDeleteView(DeleteView):
    template_name = 'main-page/post/delete_post.html'
    model = Post

    def get_success_url(self):
        return reverse('post-list')

class CommentCreateVew(CreateView):
    template_name = 'main-page/comment/create.html'
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = post
        comment.save()
        return redirect('post-detail', pk=post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        context['post'] = post
        return context


class CommentDeleteView(DeleteView):
    model = Comment
    form_class = CommentForm

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('post-list')

class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main-page/comment/edit.html'
    context_key = 'comment'

    def get_success_url(self):
        return reverse('post-list')
