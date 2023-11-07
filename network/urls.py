
from django.urls import path

from . import views

urlpatterns = [
    path('tweets/', views.posts_view, name='tweets_view'),
    path("load_users", views.load_users, name="load_users"),
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
