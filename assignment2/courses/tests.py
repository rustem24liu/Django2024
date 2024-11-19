from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from students.models import Student
from .models import Course, Enrollment
from .serializers import CourseSerializer

class CourseModelTest(TestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword', is_staff=True)
        self.student_user = User.objects.create_user(username='student', password='testpassword')
        self.student = Student.objects.create(user=self.student_user)

    def test_course_creation(self):
        course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)
        self.assertEqual(course.name, 'Math 101')
        self.assertEqual(course.instructor.username, 'teacher')
        self.assertEqual(course.description, 'Basic Mathematics')

class EnrollmentModelTest(TestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword', is_staff=True)
        self.student_user = User.objects.create_user(username='student', password='testpassword')
        self.student = Student.objects.create(user=self.student_user)
        self.course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course, instructor=self.teacher_user)
        self.assertEqual(enrollment.student.user.username, 'student')
        self.assertEqual(enrollment.course.name, 'Math 101')
        self.assertEqual(enrollment.instructor.username, 'teacher')

    def test_enrollment_unique(self):
        Enrollment.objects.create(student=self.student, course=self.course, instructor=self.teacher_user)
        with self.assertRaises(Exception):  # Ensure duplicate enrollment doesn't happen
            Enrollment.objects.create(student=self.student, course=self.course, instructor=self.teacher_user)

class CourseListViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='testpassword', is_staff=True)
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword')
        self.student_user = User.objects.create_user(username='student', password='testpassword')
        self.course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)

    def test_course_list_authenticated(self):
        self.client.login(username='admin', password='testpassword')
        response = self.client.get('/course/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['courses']), 1)

    def test_student_course_list(self):
        self.client.login(username='student', password='testpassword')
        response = self.client.get('/course/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['courses']), 0)

    def test_teacher_course_list(self):
        self.client.login(username='teacher', password='testpassword')
        response = self.client.get('/course/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['courses']), 1)


class CourseCreateViewTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='testpassword', is_staff=True)
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword')

    def test_create_course_as_admin(self):
        self.client.login(username='admin', password='testpassword')
        data = {'name': 'Science 101', 'description': 'Basic Science', 'instructor': self.teacher_user.id}
        response = self.client.post('/course/courses/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Science 101')

    def test_create_course_as_teacher(self):
        self.client.login(username='teacher', password='testpassword')
        data = {'name': 'Science 101', 'description': 'Basic Science', 'instructor': self.teacher_user.id}
        response = self.client.post('/course/courses/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class EnrollmentCreateViewTest(APITestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword')
        self.student_user = User.objects.create_user(username='student', password='testpassword')
        self.student = Student.objects.create(user=self.student_user)
        self.course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)

    def test_enroll_student(self):
        self.client.login(username='student', password='testpassword')
        data = {'course': self.course.id}
        response = self.client.post('/course/enroll/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['student_name'], 'student')
        self.assertEqual(response.data['course_name'], 'Math 101')

    def test_enroll_as_teacher(self):
        self.client.login(username='teacher', password='testpassword')
        data = {'course': self.course.id}
        response = self.client.post('/course/enroll/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TeacherSelectionViewTest(APITestCase):

    def setUp(self):
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword')
        self.student_user = User.objects.create_user(username='student', password='testpassword')
        self.student = Student.objects.create(user=self.student_user)
        self.course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)
        self.enrollment = Enrollment.objects.create(student=self.student, course=self.course, instructor=self.teacher_user)

    def test_teacher_selection_by_student(self):
        self.client.login(username='student', password='testpassword')
        data = {'teacher': self.teacher_user.id}
        response = self.client.patch(f'/course/enroll/{self.enrollment.id}/select_teacher/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_selection_as_teacher(self):
        self.client.login(username='teacher', password='testpassword')
        data = {'teacher': self.teacher_user.id}
        response = self.client.patch(f'/course/enroll/{self.enrollment.id}/select_teacher/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseCacheTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='testpassword', is_staff=True)
        self.teacher_user = User.objects.create_user(username='teacher', password='testpassword')
        self.course = Course.objects.create(name='Math 101', description='Basic Mathematics', instructor=self.teacher_user)

    def test_cache_for_course_list(self):
        self.client.login(username='admin', password='testpassword')
        response1 = self.client.get('/course/courses/')
        self.assertEqual(response1.status_code, 200)

        response2 = self.client.get('/course/courses/')
        self.assertEqual(response2.status_code, 200)