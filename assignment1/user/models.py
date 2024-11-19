from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile', verbose_name="profile")
    number = models.CharField(max_length=50, verbose_name="number", null=True, blank=True)
    birth_date = models.DateField(verbose_name='birth date', null=True, blank=True)
    avatar = models.ImageField(upload_to='user_pics', verbose_name='avatar', null=True, blank=True)
    followers = models.ManyToManyField(get_user_model(), related_name='followers', verbose_name='followers', blank=True, symmetrical=False)

    def __str__(self):
        return self.user.get_full_name()

class Follow(models.Model):
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='follower', verbose_name="follower")
    following = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following', verbose_name="following")

    def __str__(self):
        return f'{self.follower}'

