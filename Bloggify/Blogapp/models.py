from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib import admin
from django.utils import timezone

class AppUsers(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=255)  
    cover = models.ImageField(upload_to='cover_pics/', blank=True, null=True)
    blog_count = models.IntegerField
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='N',
    )

    def _str_(self):
        return self.author.username
    
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)

    def __str__(self):
        return self.title