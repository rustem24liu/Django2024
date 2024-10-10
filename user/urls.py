from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import UserDetailView, UserUpdateView, PasswordChangeView

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='profile'),
    path('profile/edit', UserUpdateView.as_view(), name='edit'),
    path('change-password', PasswordChangeView.as_view(), name='change-password'),
    path('follow/<str:username>', views.follow_user, name='follow'),
    path('unfollow/<str:username>', views.unfollow_user, name='unfollow'),
]
