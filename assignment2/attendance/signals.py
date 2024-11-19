import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
from grades.models import Grade

# Get the logger for attendance activity
logger = logging.getLogger('attendance_activity')

@receiver(post_save, sender=Attendance)
def log_attendance_marking(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Attendance marked for student {instance.student.user.username} in course: {instance.course.name}")

# Similarly, for grade updates
@receiver(post_save, sender=Grade)
def log_grade_update(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Grade updated for student {instance.student.user.username} in course: {instance.course.name} - {instance.grade}")
