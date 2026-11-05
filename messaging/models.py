from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class ThreadModel(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    
class MessageModel(models.Model):
    thread = models.ForeignKey('ThreadModel', related_name='messages', on_delete=models.CASCADE, null=True, blank=True, default=None)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='Uploads/message_images', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    read_by = models.ManyToManyField(User, related_name='read_messages', blank=True)
