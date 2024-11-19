from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from courses.models import Course, Enrollment
from students.models import Student
from django.contrib.auth import get_user_model
from .models import Grade
from django.urls import reverse

User = get_user_model()

# Create your tests here.

class GradeModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(username='teacher', password='password', is_staff=True)
        self.student = User.objects.create_user(username='student', password='password')

        self.course = Course.objects.create(name="Math 101", instructor=self.teacher)
        self.student_instance = Student.objects.create(user=self.student)
        Enrollment.objects.create(student=self.student_instance, course=self.course, instructor=self.teacher)

        self.grade = Grade.objects.create(student=self.student_instance, course=self.course, grade=90.00, teacher=self.teacher)

    def test_grade_string_representation(self):
        self.assertEqual(str(self.grade), f'{self.student_instance} - {self.course} - {self.grade.grade}')


class GradeListViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.teacher = User.objects.create_user(username='teacher', password='password', is_staff=True)
        self.student = User.objects.create_user(username='student', password='password')

        self.course = Course.objects.create(name="Math 101", instructor=self.teacher)
        self.student_instance = Student.objects.create(user=self.student)
        Enrollment.objects.create(student=self.student_instance, course=self.course, instructor=self.teacher)

        self.grade = Grade.objects.create(student=self.student_instance, course=self.course, grade=90.00, teacher=self.teacher)

        self.url = reverse('grade-list')

    def test_grade_list_view_as_teacher(self):
        self.client.login(username='teacher', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_grade_list_view_as_student(self):
        self.client.login(username='student', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_grade_list_view_permission_denied_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GradeCreateViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.teacher = User.objects.create_user(username='teacher', password='password', is_staff=True)
        self.student = User.objects.create_user(username='student', password='password')

        self.course = Course.objects.create(name="Math 101", instructor=self.teacher)
        self.student_instance = Student.objects.create(user=self.student)
        Enrollment.objects.create(student=self.student_instance, course=self.course, instructor=self.teacher)


        self.url = reverse('grade-create')

    def test_create_grade_as_teacher(self):
        self.client.login(username='teacher', password='password')
        data = {
            "student": self.student_instance.id,
            "course": self.course.id,
            "grade": 95.00
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 1)

    def test_create_grade_permission_denied_for_non_teacher(self):
        self.client.login(username='student', password='password')
        data = {
            "student": self.student_instance.id,
            "course": self.course.id,
            "grade": 95.00
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GradeUpdateViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.teacher = User.objects.create_user(username='teacher', password='password', is_staff=True)
        self.student = User.objects.create_user(username='student', password='password')

        self.course = Course.objects.create(name="Math 101", instructor=self.teacher)
        self.student_instance = Student.objects.create(user=self.student)
        Enrollment.objects.create(student=self.student_instance, course=self.course, instructor=self.teacher)

        self.grade = Grade.objects.create(student=self.student_instance, course=self.course, grade=90.00, teacher=self.teacher)

        self.url = reverse('grade-update', kwargs={'pk': self.grade.id})

    def test_update_grade_as_teacher(self):
        self.client.login(username='teacher', password='password')
        data = {"grade": 95.00}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.grade.refresh_from_db()
        self.assertEqual(self.grade.grade, 95.00)

    def test_update_grade_permission_denied_for_non_teacher(self):
        self.client.login(username='student', password='password')
        data = {"grade": 95.00}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GradeDeleteViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create users
        self.teacher = User.objects.create_user(username='teacher', password='password', is_staff=True)
        self.student = User.objects.create_user(username='student', password='password')

        self.course = Course.objects.create(name="Math 101", instructor=self.teacher)
        self.student_instance = Student.objects.create(user=self.student)
        Enrollment.objects.create(student=self.student_instance, course=self.course, instructor=self.teacher)

        self.grade = Grade.objects.create(student=self.student_instance, course=self.course, grade=90.00, teacher=self.teacher)

        self.url = reverse('grade-delete', kwargs={'pk': self.grade.id})

    def test_delete_grade_as_teacher(self):
        self.client.login(username='teacher', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Grade.objects.count(), 0)

    def test_delete_grade_permission_denied_for_non_teacher(self):
        self.client.login(username='student', password='password')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
