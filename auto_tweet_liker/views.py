from django.shortcuts import render
from .models import *
from django.http import *
from django.shortcuts import render_to_response
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from auto_tweet_liker.utils import * 
# from profanityfilter import ProfanityFilter
import tweepy
import time
import os

def index(request):
    # return render(request, "index.html")
    if check_key(request):
        return render(request, 'index.html')
    else:
        return render_to_response('login.html')

def like(request):
    counter = 0

    keyword = request.POST['search']

    # Providing tweeter API keys for accessing the API data
    # 'IeGj41fptB', 'rJiYi0wtXYvqd8RUx9medcP'

    # Adding access tokens for the tweeter account
    # '873755259780386816-lYaAmRQPoE9', 'qvwPKIUWavNQD2F8NKhbj9yd'
    # if check_key(request):
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Getting the user
    user = api.me()

    print(user.screen_name)

    # Adding keyword to search the tweets for
    search = keyword
    # Specifying the tweets limit
    numberOfTweets = 5

    # Fetching the tweets and liking them
    for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
        try:
            tweet.favorite()
            print('Tweet Liked!')
            counter = counter + 1
            time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break
    return render(request, "liked.html", {'counter': counter, 'keyword': search})
# else:
#     return render_to_response(request, "login.html")
 

def auth(request):
	# start the OAuth process, set up a handler with our details
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	# direct the user to the authentication url
	# if user is logged-in and authorized then transparently goto the callback URL
	auth_url = oauth.get_authorization_url(True)
	response = HttpResponseRedirect(auth_url)
	# store the request token
	request.session['request_token'] = oauth.request_token
	return response

def callback(request):
	verifier = request.GET.get('oauth_verifier')
	oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	token = request.session.get('request_token')
	# remove the request token now we don't need it
	request.session.delete('request_token')
	oauth.request_token = token
	# get the access token and store
	try:
		oauth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error, failed to get access token')

	request.session['access_key_tw'] = oauth.access_token
	request.session['access_secret_tw'] = oauth.access_token_secret
	print(request.session['access_key_tw'])
	print(request.session['access_secret_tw'])
	response = HttpResponseRedirect(reverse('index'))
	return response

def check_key(request):
	"""
	Check to see if we already have an access_key stored, if we do then we have already gone through
	OAuth. If not then we haven't and we probably need to.
	"""
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True