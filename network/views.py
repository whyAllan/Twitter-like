from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django import forms

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
    profile = Profile.objects.get(user=request.user.id)
    if profile:
        return render(request, "network/index.html", {
        "profile": profile,
        "post_form": PostForm(),
        'posts': Post.objects.all()
         })
    else:
        return render(request, "network/index.html", {
            "posts": Post.objects.all()
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
        return HttpResponseRedirect(reverse("index"))
    
    # Display profile page
    return render(request, "network/profile.html")
