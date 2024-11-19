from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from .models import Attendance
from courses.models import Course, Enrollment
from .serializers import AttendanceSerializer

from courses.permissions import IsTeacher


class MarkAttendanceView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsTeacher]

    def get_queryset(self):
        user = self.request.user

        if not user.groups.filter(name='Teacher').exists():
            raise PermissionDenied("You must be a teacher to mark attendance.")

        return Attendance.objects.filter(course__instructor=user)

    def perform_create(self, serializer):
        user = self.request.user
        course_id = self.kwargs['course_id']

        try:
            course = Course.objects.get(id=course_id, instructor=user)
        except Course.DoesNotExist:
            raise PermissionDenied("You can only mark attendance for your own courses.")

        student_id = self.request.data.get('student')
        if not Enrollment.objects.filter(course=course, student_id=student_id).exists():
            raise PermissionDenied("This student is not enrolled in your course.")

        serializer.save(course=course)


class ViewAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.groups.filter(name='Teacher').exists():
            raise PermissionDenied("You must be a teacher to view attendance.")

        course_id = self.kwargs['course_id']
        course = Course.objects.get(id=course_id)

        if course.instructor != user:
            raise PermissionDenied("You can only view attendance for courses you teach.")

        return Attendance.objects.filter(course=course)


class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        student = user.student

        return Attendance.objects.filter(student=student)
