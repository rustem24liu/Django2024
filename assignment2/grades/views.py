from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .pagination import GradesPagination
from .serializers import StudentCoursesGradeSerializer, GradeSerializer
from .models import Grade
# from ..courses.models import Enrollment
from courses.models import Enrollment

from courses.permissions import IsTeacher

from courses.permissions import IsStudent
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


# from ..courses.permissions import IsStudent


# Create your views here.

class GradeListView(generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GradesPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['course', 'student', 'grade', 'date']
    search_fields = ['course__name']
    ordering_fields = ['grade', 'date']
    permission_classes = [IsAuthenticated, IsTeacher | IsAdminUser | IsStudent]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Admin').exists():
            return Grade.objects.all()

        if user.groups.filter(name='Student').exists():
            return Grade.objects.filter(student__user=user)

        if user.groups.filter(name='Teacher').exists():
            return Grade.objects.filter(course__instructor=user)


        raise PermissionDenied("You do not have permission to perform this action.")

class GradeCreateView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdminUser]
    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Admin').exists():
            return Grade.objects.all()

        if user.groups.filter(name='Student').exists():
            return Grade.objects.filter(student__user=user)

        if user.groups.filter(name='Teacher').exists():
            return Grade.objects.filter(course__instructor=user)
            # return Grade.objects.filter(student__user=user)
            # return Grade.objects.all()

        raise PermissionDenied("You do not have permission to perform this action.")

    def perform_create(self, serializer):
        user = self.request.user

        if not user.groups.filter(name='Teacher').exists():
            raise PermissionDenied("Only teachers can assign grades.")

        course = serializer.validated_data['course']
        if course.instructor != user:
            raise PermissionDenied("You can only assign grades to students in your own courses.")

        student = serializer.validated_data['student']
        if not Enrollment.objects.filter(course=course, student=student).exists():
            raise PermissionDenied("This student is not enrolled in the selected course.")

        serializer.save(teacher=user)

class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdminUser | IsStudent]

class GradeUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdminUser]

class GradeDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdminUser]

class StudentCoursesGradesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id, *args, **kwargs):
        grades = Grade.objects.filter(student__id=student_id)
        serializer = StudentCoursesGradeSerializer(grades, many=True)

        response_data = {}
        for grade_data in serializer.data:
            course_name = grade_data['course_name']
            response_data[course_name] = {
                'grade': grade_data['grade'],
                'grade_letter': grade_data['grade_letter']
            }

        return Response(response_data)