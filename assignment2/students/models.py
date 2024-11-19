

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student', default=1)
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, null=True, blank=True)
    dob = models.DateTimeField(null=True, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Student: {self.name}'