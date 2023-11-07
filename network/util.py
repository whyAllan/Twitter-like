from .models import User, Profile, Post
from django.core.paginator import Paginator
from django.shortcuts import render

"""
    htmx views
"""

def posts_view(request):
    """ Dispaly posts """
    # Filter can be either 'not', 'following', 'replies' or a username
    # key1 = page number key2 = filter key3 = tweet id
    page = request.GET.get('key1')
    if page == '':
        page = 1
    filter = request.GET.get('key2')
    if filter == 'not':
        context = Post.objects.all().order_by("-created_at")
    elif filter == 'following':
        context =  Post.objects.filter(poster__in=Profile.objects.get(user=request.user.id).following.all()).order_by('-created_at')
    elif filter == 'replies':
        tweet = request.GET.get('key3')
        context =  Post.objects.filter(reply=tweet).order_by('-created_at')
    else:
        context =  Post.objects.filter(poster=Profile.objects.get(user=User.objects.get(username=filter))).order_by('-created_at')
    paginator = Paginator(context, 10)
    return render(request, "network/tweets.html", {
        "posts": paginator.page(page),
        "filter": filter,
        "page": page
    })

def load_users(request):
    """ Load users with pagination conbined with htmx """
    # key1 = profile, key2 = filter, key3 = page number
    profile = request.GET.get('key1')
    filter = request.GET.get('key2')
    pagenum = request.GET.get('key3')
    
    profile = Profile.objects.get(user=User.objects.get(username=profile))
    if filter == 'following':
        result = profile.following.all().order_by('user__username')

    elif filter == 'followers':
       result = profile.followers.all().order_by('user__username')

    pagination = Paginator(result, 10)
    users = pagination.page(pagenum)
    # render html to be render in the profile page
    return render(request, "network/render_users.html", {
        "users": users,
        "pagenum": pagenum,
        "filter": filter,
        "profile": profile
    })
    
def follow_unfollow(request, username):
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
        return render(request, "network/render_users.html", {
            "users": Profile.objects.filter(user=User.objects.get(username=username))
            })