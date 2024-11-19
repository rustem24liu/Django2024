from django.db import models
from students.models import Student
from courses.models import Course
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'groups__name': 'Teacher'})

    def __str__(self):
        return f'{self.student} - {self.course} - {self.grade}'