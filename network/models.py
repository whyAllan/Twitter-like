from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField("self", blank=True)
    followers = models.ManyToManyField("self", blank=True)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username
    
    def is_valid_profile(self):
        return not self.followers.filter(user=self.user).exists() and not self.following.filter(user=self.user).exists()

class Post(models.Model):
    post = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.post

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="comments_likes")


    def __str__(self):
        return self.comment