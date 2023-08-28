from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_img',
                              default='blank-profile-picture.png')
    bio = models.TextField(blank=True)
    aboutAuthor = models.CharField(max_length=600, blank=True)
    createdAt = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return self.user.username


class BlogPosts(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    post_img = models.ImageField(upload_to="post_img")
    description = models.CharField(max_length=4500)
    category = models.CharField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=timezone.now)
    updatedAt = models.DateTimeField(auto_now=timezone.now)

    # def __str__(self):
    #     return self.user
