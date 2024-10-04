
from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list_view, name='posts'),
]
