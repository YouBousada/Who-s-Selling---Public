from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    asking_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/post_images/', blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null = True, blank = True, related_name='posts')

    def __str__(self):
        return self.title
