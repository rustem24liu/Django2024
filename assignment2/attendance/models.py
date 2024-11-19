from django.db import models

from courses.models import Course
from students.models import Student


# Create your models here.

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('D', 'Done'),
        ('A', 'Absent'),
        ('E', 'Excused'),
        ('L', 'Late'),
    ]
    status = models.CharField(max_length=1, choices=status_choices)

    def __str__(self):
        return f'{self.student} - {self.course} - {self.date} - {self.status}'