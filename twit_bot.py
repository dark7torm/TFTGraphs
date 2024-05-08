import tweepy
import os
api_key =  os.environ["TWIT_API"]
api_secret = os.environ["TWIT_API_SECRET"]
bearer = os.environ["TWIT_BEARER"]
access = os.environ["TWIT_ACCESS"]
access_secret = os.environ["TWIT_ACCESS_SECRET"]


client = tweepy.Client(bearer, api_key, api_secret, access, access_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access, access_secret)

api = tweepy.API(auth)

client.create_tweet(text = "test")