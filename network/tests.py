from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        # Create users
        User.objects.create(username='user1')
        User.objects.create(username='user2')

        # Create profiles
        id2 = User.objects.get(username='user2').id
        Profile.objects.create(user=User.objects.get(username='user2')).followers.add(Profile.objects.get(user=id2))
        Profile.objects.create(user=User.objects.get(username='user1')).followers.add(Profile.objects.get(user=id2))

    def test_is_valid_profile(self):
        # user1 should be valid and user2 should not 
        self.assertTrue(Profile.objects.get(user=User.objects.get(username='user1')).is_valid_profile())
        profile = Profile.objects.get(user=User.objects.get(username='user2'))
        self.assertFalse(profile.is_valid_profile())

