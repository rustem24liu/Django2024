"""
URL configuration for source project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from user.views import about_user, index
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Apishka",
        default_version='v1',
        description="University management system, created with Django",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="temirgalirustem05@gmail.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', index, name='main-page'),
    path('admin/', admin.site.urls),
    path('accounts/', include('user.urls')),
    path('course/', include('courses.urls')),
    path('grades/', include('grades.urls')),
    path('student/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('notifications/', include('notifications.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
