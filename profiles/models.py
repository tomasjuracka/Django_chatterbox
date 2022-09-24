from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(null=True)
    photo = models.TextField(null=True)
    last_seen = models.DateTimeField(auto_now=True)
    signed_up = models.DateTimeField(auto_now_add=True)


class OnlineUsers(models.Model):
    logged = models.OneToOneField(User, on_delete=models.CASCADE)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
