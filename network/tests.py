from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        # Create users
        User.objects.create(username='user1')
        User.objects.create(username='user2')
        # User1 follows user2 and user2 follows user2 user 2 should be invalid
        Profile.objects.get(user=User.objects.get(username='user1')).following.add(Profile.objects.get(user=User.objects.get(username='user2')))
        Profile.objects.get(user=User.objects.get(username='user2')).following.add(Profile.objects.get(user=User.objects.get(username='user2')))

    def test_is_valid_profile(self):
        # user1 should be valid and user2 too
        self.assertTrue(Profile.objects.get(user=User.objects.get(username='user1')).is_valid_profile())
        profile = Profile.objects.get(user=User.objects.get(username='user2'))
        self.assertFalse(profile.is_valid_profile())

