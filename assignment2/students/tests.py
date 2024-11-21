from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core import mail
from students.models import Student
# from notifications.tasks import daily_attendance_reminder


class StudentModelTest(TestCase):
    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            email='ernur@gmail.com',
            username='ernur',
            password='admin',
        )

        self.student = Student.objects.create(
            user=self.user,
            name="Yeraly Kumargali",
            email="ernur@gmail.com"
        )

    def test_student_creation(self):
        self.assertEqual(self.student.user.username, 'ernur')
        self.assertEqual(self.student.name, 'Yeraly Kumargali')

    def test_student_email(self):
        self.assertEqual(self.student.email, 'ernur@gmail.com')
