
from django.urls import path

from . import views

urlpatterns = [
    path('tweets/?page=<int:page>/', views.PostListView.as_view(), name='post_list_page'),
    path("tweets/", views.PostListView.as_view(), name="tweets_view"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.create_profile, name="create_profile"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following_tweets, name="following_tweets")
]
