from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .pagination import CoursePagination
from .permissions import IsTeacher, IsStudent
from .models import *
from .serializers import *
from students.serializers import StudentSerializer
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.decorators import method_decorator


# Create your views here.

# class CoursePagination(PageNumberPagination):
#     page_size = 1
#     page_size_query_param = 'page_size'
#     max_page_size = 5
# @cache_page(60 * 15)
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination
    filter_backends = [OrderingFilter, SearchFilter]
    filterset_fields = ['instructor', 'name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 15))
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser or user.is_staff:
            courses = Course.objects.all()

            serializer = CourseSerializer(courses, many=True)

            return Response({
                "role": "Admin/Superuser",
                "courses": serializer.data
            })

        elif user.groups.filter(name="Student").exists():
            student = user.student
            enrollments = Enrollment.objects.filter(student=student)
            courses = [enrollment.course for enrollment in enrollments]

            serializer = CourseSerializer(courses, many=True)

            return Response({
                "role": "Student",
                "courses": serializer.data
            })

        elif user.groups.filter(name="Teacher").exists():
            courses = Course.objects.filter(instructor=user)

            course_data = []
            for course in courses:
                enrollments = Enrollment.objects.filter(course=course)
                students = [enrollment.student for enrollment in enrollments]

                student_serializer = StudentSerializer(students, many=True)

                course_data.append({
                    'course': CourseSerializer(course).data,
                    'students': student_serializer.data
                })

            return Response({
                "role": "Teacher",
                "courses": course_data
            })

        else:
            raise PermissionDenied("You do not have permission to access this view.")

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

class CourseDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser]

class EnrollmentCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent | IsAdminUser]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Student').exists():
            return Enrollment.objects.filter(student=user.student)

        if user.is_staff:
            return Enrollment.objects.all()

        raise PermissionDenied('You do not have permission to view this data')

    def perform_create(self, serializer):
        user = self.request.user

        if user.groups.filter(name='Student').exists():
            serializer.save(student=user.student)

        elif user.is_staff:
            serializer.save()

        else:
            raise PermissionDenied('You do not have permission to view this data')

class TeacherSelectionView(generics.UpdateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = TeacherSelectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_object(self):
        user = self.request.user
        course_id = self.kwargs['course_id']
        try:
            enrollment = Enrollment.objects.get(student=user.student, course_id=course_id)
        except Enrollment.DoesNotExist:
            raise PermissionDenied("You are not enrolled in this course.")
        # enrollment = Enrollment.objects.get(student=user.student, course__id=self.kwargs['course_id'])
        return enrollment
    #
    def get_serializer_context(self):
        context = super().get_serializer_context()
        course = self.get_object().course
        context['course'] = course
        student = self.get_object().student
        context['student'] = student
        return context

    def perform_update(self, serializer):
        user = self.request.user

        if not user.groups.filter(name='Student').exists():
            raise PermissionDenied("Only students can select a teacher.")

        serializer.save(student=user.student)
