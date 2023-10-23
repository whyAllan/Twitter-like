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
            'post': forms.TextInput(attrs={
                'class': 'form-control-plaintext',
                'id': 'floatingEmptyPlaintextInput',
                'placeholder': "What's good?"
            })
        }

def index(request):
    """ Display and create a new Post """
    if request.method == "POST":
        # Create a new Post
        contente = PostForm(request.POST)
        if contente.is_valid():
            post = contente.save(commit=False)
            post.poster = request.user
            post.save()
        return HttpResponseRedirect(reverse("index"))

    # Display homepage
    if request.user.is_authenticated:
        return render(request, "network/index.html", {
        "profile": Profile.objects.get(user=request.user.id),
        "post_form": PostForm()
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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def create_profile(request):
    if request.method == "POST":
         # Create a new Profile object with the submitted data
        bio = request.POST.get("bio")
        pic = request.POST.get('pic')
        user = request.user
        profile = Profile(user=user, bio=bio, profile_pic=pic)
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/profile.html")
