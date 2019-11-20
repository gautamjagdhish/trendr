from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.twitter_list, name='twitter_list'),
    path('tweet/<int:id>/tweet_edit', views.tweet_edit, name='tweet_edit'),
    path('tweet/<int:id>/tweet_delete', views.tweet_delete, name='tweet_delete'),
    path('tweet/<int:id>/<str:slug>/', views.tweet_detail, name='tweet_detail'),
    path('tweet/create/', views.tweet_create, name='tweet_create'),

    #path('login/', views.user_login, name='user_login'),
    path('login/', auth_views.LoginView.as_view(template_name='twitter/login.html'), name='user_login'),
    path('accounts/login/', views.user_login, name='accounts_user_login'),
    path('accounts/profile/', views.user_login, name='accounts_profile_user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('like/', views.like_tweet, name='like_tweet'),
    path('like_tweets/', views.user_liked_tweets, name='user_liked_tweets'),
    path('about/', views.about, name='about'),
    path('trending/', views.trending, name='trending'),
    path('user_tweets/<str:username>', views.user_tweets, name='user_tweets'),
    path('hashtag_tweets/<str:hashtag>', views.hashtag_tweets, name='hashtag_tweets'),

]