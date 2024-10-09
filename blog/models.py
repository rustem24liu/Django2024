from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='authors')

    def __str__(self):
        return f'{self.pk} - {self.name}'

class Post(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(max_length=2000, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    image = models.ImageField(upload_to='post-images', null=True, blank=True)

    def __str__(self):
        return f'{self.pk} - {self.title} /n {self.author}'

class Comment(models.Model):
    body = models.TextField(max_length=2000, null=False, blank=False, verbose_name="Comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    def __str__(self):
        return f'{self.pk} - {self.body[:20]} /n {self.author} post: {self.post}'