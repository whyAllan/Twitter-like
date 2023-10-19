from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return self.user.username
    # Assert that the user cannot follow themselves
    def is_valid_profile(self):
        return self.following.filter(username=self.user.username).exists() and not self.followers.filter(username=self.user.username).exists()

    # Assert that the user cannot follow the same user twice
    def is_following(self, user):
        return self.following.filter(username=user.username).exists()


class Post(models.Model):
    post = models.TextField()
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.post

class Comments(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="comments_likes")


    def __str__(self):
        return self.comment