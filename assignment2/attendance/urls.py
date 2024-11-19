from django.urls import path
from .views import MarkAttendanceView, ViewAttendanceView, StudentAttendanceView

urlpatterns = [
    path('course/<int:course_id>/mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
    path('view/<int:course_id>/', ViewAttendanceView.as_view(), name='view-attendance'),
    path('student/', StudentAttendanceView.as_view(), name='student-attendance'),
]
