
from django.urls import path

from . import views, util

urlpatterns = [
    path('tweets/', util.posts_view, name='tweets_view'),
    path("follow_unfollow/<str:username>", util.follow_unfollow, name="follow_unfollow"),
    path("load_users", util.load_users, name="load_users"),
    path("", views.index, name="index"),
    path("replies/<int:post_id>", views.replies, name="replies"),
    path("change/<int:post_id>", views.edit, name="change"),
    path("likes/<int:post_id>", views.likes, name="like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.create_profile, name="create_profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following_tweets, name="following_tweets")
]
