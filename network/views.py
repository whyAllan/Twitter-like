from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django import forms
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import User, Profile, Post, Comments

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post']
        widgets = {
            'post': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'What is on your mind?',
                'id': 'floatingTextarea',
                'style':'width: 300px; height: 100px; border-radius: 10px; margin-top: 30%; margin-left: 10px;'
            })
        }
class PostListView(ListView):
    paginate_by = 10
    model = Post
    context_object_name = 'posts'
    template_name = 'network/tweets.html'

    def get_queryset(self):
        queryset = self.model.objects.order_by('-created_at')
        paginator = Paginator(queryset, self.paginate_by)

        page_number = self.request.GET.get('page')
        if page_number == '':
            return queryset
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        posts = paginator.get_page(page_number)
        return posts

def index(request):
    """ Display and create a new Post """
    if request.method == "POST":
        # Create a new Post
        contente = PostForm(request.POST)
        if contente.is_valid():
            post = contente.save(commit=False)
            post.poster = Profile.objects.get(user=request.user.id)
            post.save()
        return HttpResponseRedirect(reverse("index"))

    # Display homepage
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
        "profile": Profile.objects.get(user=request.user.id),
        "post_form": PostForm(),
        })
    else:
        return render(request, "network/index.html", {
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        # Create Profile
        profile  = Profile.objects.create(user=user)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def create_profile(request):
    """ Create and update profile """
    if request.method == "POST":
         # Create or update profile
        bio = request.POST.get("bio")
        pic = request.POST.get('pic')
        user = request.user
        try:
            profile = Profile(user=user, bio=bio, profile_pic=pic)
            profile.save()
        except IntegrityError:
            profile = Profile.objects.get(user=user)
            profile.bio = bio
            profile.profile_pic = pic
            profile.save()
        return HttpResponseRedirect(reverse("profile", args=(user.username,)))
    
    # Display profile page
    return render(request, "network/profile_create.html")

def profile(request, username):
    """ Display profile/follow and unfollow user """
    if request.method == "POST":
        # Follow or unfollow
        follow = request.POST['follow']
        if follow == 'follow':
            profile = Profile.objects.get(user=User.objects.get(username=username))
            user = Profile.objects.get(user=request.user.id)
            profile.followers.add(user)
            user.following.add(profile)
        
        elif follow == 'unfollow':
            profile = Profile.objects.get(user=User.objects.get(username=username))
            user = Profile.objects.get(user=request.user.id)
            profile.followers.remove(user)
            user.following.remove(profile)
        return HttpResponseRedirect(reverse("profile", args=(username,)))
    # Display profile
    return render(request, "network/display_profile.html", {
        "profile": Profile.objects.get(user=User.objects.get(username=username)),
        "posts": Post.objects.filter(poster=Profile.objects.get(user=User.objects.get(username=username))).order_by('-created_at')
    })

def following_tweets(request):
    """ Display following tweets """
    return render(request, "network/index.html", {
        "profile": Profile.objects.get(user=request.user.id),
        "post_form": PostForm(),
        "posts": Post.objects.filter(poster__in=Profile.objects.get(user=request.user.id).following.all()).order_by('-created_at')
    })