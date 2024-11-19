from django.urls import path

from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('courses/', cache_page(60*15)(CourseListView.as_view()), name = 'courses'),
    path('create/', CourseCreateView.as_view(), name = 'create-course'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name = 'course-detail'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name = 'course-update'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('enroll/', EnrollmentCreateView.as_view(),name='enroll-student'),
    path('select_teacher/<int:course_id>/', TeacherSelectionView.as_view(), name='select-teacher'),
]