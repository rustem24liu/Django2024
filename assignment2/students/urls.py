from django.urls import path
from grades.views import StudentCoursesGradesView

urlpatterns = [
    path('s/<int:pk>/grades/', StudentCoursesGradesView.as_view(), name='student-grades'),
]