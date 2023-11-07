from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField('self', blank=True, related_name="following_to", symmetrical=False)
    followers = models.ManyToManyField('self', blank=True, related_name="followed_by", symmetrical=False)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)

    

    def __str__(self):
        return self.user.username
    # Assert that the user cannot follow themselves
    def is_valid_profile(self):
        return not self.following.filter(user=self.user.pk).exists() and not self.followers.filter(user=self.user.pk).exists()

    # Assert that the user cannot follow the same user twice
    def is_following(self, user):
        return self.following.filter(username=user.username).exists()

# Create a Profile when a User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Post(models.Model):
    post = models.TextField()
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(Profile, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="replies")  

    def __str__(self):
        return self.post
