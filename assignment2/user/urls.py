from django.contrib import admin
from django.urls import path, include
from rest_framework import authentication
# from setuptools.extern import names

from .views import Authentication, about_user
from .views import register_view, UserProfileUpdate

urlpatterns = [
    path('authentication/', Authentication.as_view(), name='authentication'),
    path('log/', include('rest_framework.urls')),
    path('register/', register_view, name='register'),
    path('profile/', about_user, name='profile'),
    path('profile/update/', UserProfileUpdate.as_view(), name='profile-update'),
]
