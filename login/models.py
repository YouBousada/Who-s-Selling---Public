from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    sustainability_interests = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/profile_pictures/', blank=True, null=True)
    is_new_user = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username