from django.db import models
from django.contrib.auth.models import User

class APIRequestLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.path} - {self.method}"

class CourseViewLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_id = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} viewed course {self.course_id}"