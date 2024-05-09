import tweepy
import os
from api_test import rank_finder
api_key =  os.environ["TWIT_API"]
# api_key = 'LzS1qwmphpoIFLR16TkESPaz4'
api_secret = os.environ["TWIT_API_SECRET"]
# api_secret = '2NZcMYcy6PyNP5kRa86KdMXMnXSOLvnSl228nxmtiBR5wsjr1i'
bearer = os.environ["TWIT_BEARER"]
# bearer = 'AAAAAAAAAAAAAAAAAAAAAHHQtgEAAAAA1y8XSXH1dZdq1WNAwYTj0tL5%2FTI%3DNnU6spzmKUWCbGlGyQvQA9OpG2hJsXVdrbf7XdCsV3MTzNLxXO'
access = os.environ["TWIT_ACCESS"]
# access = '1788257350769422336-22LkKNNwWT15877MGXGCprvhzXHzXS'
# access_secret = 'c8EoSrODgO5sh6dTVpDefbu53Dg5t0JQaPngglbsKNbua'
access_secret = os.environ["TWIT_ACCESS_SECRET"]

# ren + jisung + sean + owen id
test_ids = ["1dq1hI89Zgd__zcs8qkr3YaKdK35R4wj20YNB8ELdJL5_55XGPAch6g0KEiAAwFpfkeMjEnQ5HrWOg",
            # "_Mgiig0pdFVXxA2btc4XjF_hVSOW16JzLhZiBZRi6LJdxt-QAZJD5fIY7sGcmKfIzJp37HjQggTR7A",
            "WnHv1ZvlirRiQ6dwX7U8YPuSSElqhbcBhI3QdXbfGh7-NVzPUhrSuUSecKfbk8khPiexI9KFyIS3DQ",
            "F9rgc1D5JAL9w71D8KCa-5z3z9swgTdQcis2-cMu3YZenOT66RjFm-AsDqqA7X1gpe7odktx4f8WwA"]



client = tweepy.Client(bearer, api_key, api_secret, access, access_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access, access_secret)

api = tweepy.API(auth)

post_times_et = [(6, 0), (18, 0)]
print(api_key, api_secret, bearer, access, access_secret)
# bot methods: client.create_tweet, client.like, client.retweet, client.create_tweet
for id in test_ids:
    output = rank_finder(id)
    formatted = ' '.join(map(str, output))
    client.create_tweet(text = formatted)