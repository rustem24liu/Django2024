
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostListVies, PostDetailView, PostUpdateView, PostDeleteView, PostCreateView, CommentUpdateView, \
    CommentDeleteView, CommentCreateVew

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', PostListVies.as_view(), name='post-list'),
    path('post-edit/<int:pk>/', PostUpdateView.as_view(), name='post-edit'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('create-post/', PostCreateView.as_view(), name='create-post'),
    path('comment/<int:pk>/edit', CommentUpdateView.as_view(), name='comment-edit'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comment', CommentCreateVew.as_view(), name='comment-create'),
]
