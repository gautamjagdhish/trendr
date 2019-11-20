from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from datetime import datetime
from .models import Tweet, Profile
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
import operator, collections
from django.dispatch import receiver
from django.db.models.signals import post_save



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save()





def twitter_list(request):
	tweets = Tweet.objects.all().order_by('-id')
	query = request.GET.get('q')
	if query:
		tweets = Tweet.objects.filter(
		Q(title__icontains=query)|
		Q(author__username=query)|
		Q(content__icontains=query)|
		Q(hashtag__icontains=query)
		)
	context = {
	'title' : 'Twitter-Home',
	'tweets' : tweets,
	}
	return render(request, 'twitter/twitter_list.html', context)


def tweet_detail(request, id, slug):
	tweet = get_object_or_404(Tweet, id=id, slug=slug)
	is_liked = False
	if tweet.likes.filter(id=request.user.id).exists():
		is_liked = True
	context = {
		'tweet' : tweet,
		'title' : 'Twitter-Detail',
		'is_liked' : is_liked,
		'total_likes' : tweet.total_likes(),
	}
	return render(request, 'twitter/tweet_detail.html', context)

def tweet_create(request):
	if request.method == 'POST':
		form = TweetCreateForm(request.POST)
		if form.is_valid():
			tweet = form.save(commit=False)
			tweet.author = request.user
			tweet.save()
			messages.success(request, "Your Tweet has been successfully tweeted.")
			return redirect('twitter_list')
	else:	
		form = TweetCreateForm()
		
	context = {
		'form' : form
	}
	return render(request, 'twitter/tweet_create.html', context)

def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request, user)
					messages.success(request, "Your are logged In.")
					return HttpResponseRedirect(reverse('twitter_list'))
				else:
					return HttpResponse("User is not active")
			else:
				return HttpResponse("User is None")
	else:
		form = UserLoginForm()
	context = {
		'form' : form,
	}
	return render(request, 'twitter/login.html', context)

def user_logout(request):
	logout(request)
	messages.warning(request, "Your have been Logged Out.")
	return redirect("twitter_list")

# def register(request):
# 	if request.method == 'POST':
# 		form = UserRegistrationForm(request.POST or None)
# 		if form.is_valid():
# 			new_user = form.save(commit=False)
# 			new_user.set_password(form.cleaned_data['password'])
# 			new_user.save()
# 			Profile.objects.create(user=new_user)
# 			messages.success(request, "Your account has been created successfully. Now you can Log In.")
# 			return redirect('twitter_list')
# 	else:
# 		form = UserRegistrationForm()
# 	context = {
# 		'form' : form,
# 	}
# 	return render(request, 'twitter/register.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'twitter/register.html', {'form': form})

# @login_required
# def edit_profile(request):
# 	if request.method == "POST":
# 		user_form = UserEditForm(data = request.POST or None, instance=request.user)
# 		profile_form = ProfileEditForm(data = request.POST or None, instance=request.user.profile, files=request.FILES)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			user_form.save()
# 			profile_form.save()
# 			messages.success(request, "Your Profile has been successfully Updated.")
# 			return HttpResponseRedirect(reverse("edit_profile"))
# 	else:
# 		user_form = UserEditForm(instance=request.user)
# 		profile_form = ProfileEditForm(instance=request.user.profile)
# 	context = {
# 		'user_form' : user_form,
# 		'profile_form' : profile_form,
# 	}
# 	return render(request, 'twitter/edit_profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'twitter/edit_profile.html', context)

@login_required
def tweet_edit(request, id):
	tweet = get_object_or_404(Tweet, id=id)
	if tweet.author != request.user:
		raise Http404
	if request.method == "POST":
		form = TweetEditForm(request.POST or None, instance = tweet)
		if form.is_valid():
			form.save()
			messages.success(request, "Your Tweet has been successfully Updated.")
			return HttpResponseRedirect(tweet.get_absolute_url())
	else:
		form = TweetEditForm(request.POST or None, instance = tweet)
	context = {
		'form' : form,
		'tweet' : tweet,
	}
	return render(request, 'twitter/tweet_edit.html',context)


@login_required
def like_tweet(request):
	tweet = get_object_or_404(Tweet, id=request.POST.get('tweet_id'))
	is_liked = False
	if tweet.likes.filter(id=request.user.id).exists():
		tweet.likes.remove(request.user)
		is_liked = False
	else:
		tweet.likes.add(request.user)
		is_likes = True
	return HttpResponseRedirect(tweet.get_absolute_url())

def user_liked_tweets(request):
	user = request.user
	liked_tweets = user.likes.all()
	context = {
		'liked_tweets' : liked_tweets
	}
	return render(request, 'twitter/user_liked_tweets.html', context)


@login_required
def tweet_delete(request, id):
	tweet = get_object_or_404(Tweet, id=id)
	if tweet.author != request.user:
		raise Http404
	tweet.delete()
	messages.warning(request, "Your Tweet has been successfully DELETED.")
	return redirect('twitter_list')



def about(request):
    return render(request, 'twitter/about.html')


def trending(request):
	limit = timezone.now() - timezone.timedelta(hours=12)
	print(limit)
	listi = []
	for j in Tweet.objects.all():
		if j.updated > limit: #you can change update or created here
			listi.append(j)
	print(listi)
	dicti = {}
	for ii in listi:
		if ii.hashtag not in dicti:
			dicti[ii.hashtag] = 1
		else:
			dicti[ii.hashtag] = dicti[ii.hashtag] + 1
	print(dicti)
	sorted_x = sorted(dicti.items(), key=operator.itemgetter(1), reverse=True)
	print(sorted_x)
	limited_x = []
	if len(sorted_x) > 15:
		for mo in range(15):
			limited_x.append(sorted_x(mo))
	else:
		limited_x = sorted_x

	hashtags = collections.OrderedDict(limited_x)
	print(hashtags)
	context = {
		'hashtags' : hashtags
	}
	return render(request, 'twitter/trending.html', context)


def user_tweets(request, username):
	user = get_object_or_404(User, username=username)
	tweets = Tweet.objects.filter(author=user)
	context = {
		'tweets' : tweets,
		'username' : username
	}
	return render(request, 'twitter/user_tweets.html', context)


def hashtag_tweets(request, hashtag):
	tweets = Tweet.objects.filter(hashtag=hashtag)
	context = {
		'tweets' : tweets,
		'hashtag' : hashtag
	}
	return render(request, 'twitter/hashtag_tweets.html', context)