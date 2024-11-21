from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core import mail
from notifications.tasks import daily_attendance_reminder, grade_update_notification, weekly_performance_summary
from students.models import Student
from grades.models import Grade
from attendance.models import Attendance
from courses.models import Course, Enrollment  # Assuming you have a Course and Enrollment model
from datetime import datetime, timedelta

class NotificationTasksTestCase(TestCase):
    def setUp(self):

        User = get_user_model()

        self.instructor = User.objects.create_user(
            email='avinash@gmail.com',
            username='avinash',
            password='admin',
        )

        self.user = User.objects.create_user(
            email='azamat@gmail.com',
            username='azamat',
            password='admin',
        )

        self.student = Student.objects.create(
            user = self.user,
            name='azamat',
            email='azamat@gmail.com',

        )

        self.course = Course.objects.create(
            name="Calculus 1",
            description="Introduction to Calculus",
            instructor=self.instructor
        )

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
        )

        self.grade = Grade.objects.create(
            student=self.student,
            course=self.course,
            grade=89,
            teacher=self.instructor
        )

        self.attendance = Attendance.objects.create(
            student=self.student,
            course=self.course,
            status="D"
        )

    def test_daily_attendance_reminder(self):
        # Call the task synchronously
        result = daily_attendance_reminder.apply()

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Daily Attendance Reminder', mail.outbox[0].subject)
        self.assertIn(self.student.email, mail.outbox[0].to)

        # Verify task result
        self.assertIn('Sent reminders to 1 students.', result.result)

    def test_grade_update_notification(self):
        result = grade_update_notification.apply(args=[self.student.id, 'Calculus 1', 'A'])

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Grade Update Notification', mail.outbox[0].subject)
        self.assertIn('Your grade for Calculus 1 has been updated to A', mail.outbox[0].body)

        self.assertIn(f'Grade notification sent to {self.student.name}.', result.result)

    def test_weekly_performance_summary(self):

        result = weekly_performance_summary.apply()

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Weekly Performance Report', mail.outbox[0].subject)
        self.assertIn('Weekly Performance Summary for azamat', mail.outbox[0].body)

        self.assertIn('Sent weekly performance summaries to 1 students.', result.result)

