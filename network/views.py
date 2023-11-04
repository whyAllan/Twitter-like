from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from .models import User, Profile, Post
from django.contrib import messages
import urllib.parse
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

def posts_view(request, page, filter):
    """ Dispaly posts """
    # Filter can be either 'not', 'following' or a username
    filter = str(filter)
    if filter == 'not':
        context = Post.objects.all().order_by("-created_at")
    elif filter == 'following':
        context =  Post.objects.filter(poster__in=Profile.objects.get(user=request.user.id).following.all()).order_by('-created_at')
    else:
        context =  Post.objects.filter(poster=Profile.objects.get(user=User.objects.get(username=filter))).order_by('-created_at')
    paginator = Paginator(context, 10)
    return render(request, "network/tweets.html", {
        "posts": paginator.page(page),
        "filter": filter,
        "page": page
    })


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
        "page": 0,
        "filter": 'not'
        })
    else:
        return render(request, "network/index.html", {
            "page": 0,
            "filter": 'not'
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
        "filter": username,
        "page": 0
    })

def following_tweets(request):
    """ Display following tweets """
    return render(request, "network/index.html", {
        "profile": Profile.objects.get(user=request.user.id),
        "post_form": PostForm(),
        "filter": 'following',
        "page": 0
    })

def likes(request, post_id):
    """ Update likes """
    if request.user.is_authenticated:
        user = Profile.objects.get(user=request.user.id)
        tweet = Post.objects.get(id=post_id)
        if tweet.likes.filter(id=user.id).exists():
            tweet.likes.remove(user)
        else:
            tweet.likes.add(user)
    else:
        return HttpResponse("you must be logged in")
    like = Post.objects.get(id=post_id).likes.count()
    return HttpResponse(like)

def edit(request, post_id):
    """ Edit or delete post """
    if request.method == "PUT":
        content = urllib.parse.unquote(request.body.decode('utf-8').split('=')[1])
        post = Post.objects.get(id=post_id)
        post.post = content
        post.save()
        return HttpResponse(f'<p class="card-text" id="post{post_id}"> {content}</p>')
    pass