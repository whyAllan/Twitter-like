from django.test import TestCase, Client
from django.db.models import Max

from .models import Profile, User

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        # Create two users
        User.objects.create(username='user1')
        Profile.objects.create(user=User.objects.get(username='user1'))
        User.objects.create(username='user2')
        Profile.objects.create(user=User.objects.get(username='user2'))

    def test_profile(self):
         # Assert that users can't follow themselves
        profile = Profile.objects.get(user__username='user1')
        profile.follow(profile)  
        self.assertFalse(profile.is_valid_profile())

    # Assert that users can follow other users
    def test_profile(self):
        # Assert that users can follow other users
        profile1 = Profile.objects.get(user__username='user1')
        profile2 = Profile.objects.get(user__username='user2')
        profile1.following.add(profile2)
        self.assertTrue(profile1.is_valid_profile())


