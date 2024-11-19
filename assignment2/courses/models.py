from django.db import models
from django.contrib.auth.models import User, Group
from students.models import Student

# Create your models here.

def teacher_queryset():
    return User.objects.filter(groups__name="Teacher")


class Course(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    instructor = models.ForeignKey(User , null=True,  on_delete=models.SET_NULL, related_name="courses", limit_choices_to={'groups__name': "Teacher"})

    def __str__(self):
        return f'Course: {self.name}'

# There we can do like, student will be able to enroll to the courses like adding fields such credit and prereq,
# but it is al ot of work, but it is possible if we have more time

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='enrollments', limit_choices_to={'groups__name': 'Teacher'})
    enrollment_date = models.DateTimeField(auto_now_add=True)



