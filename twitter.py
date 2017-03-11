from flask import Flask
app = Flask(__name__)

###Tweepy###
import tweepy

#Create variables for each key, secret, token
consumer_key = 'hrABYWoeNcdDgyMYUPqlcITNi'
consumer_secret = '8KkiJEgeJySQ8ZFDA2ywHPx2cagifHqiXS7jxcsCWDtLPGV59K'
access_token = '838796084038230016-L8xC5JUjkDxUvfNJR4iZACE5QIKlXMG'
access_token_secret = 'jhQC3kWgc8SbkmlMnJ5965UDddeV61EbGbqcUnfzI3DuQ'

#Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


public_tweets = api.home_timeline()
tweetslist = []
#for tweet in public_tweets:
	#print(tweet.text)
###########



@app.route("/")
def hello():
    return public_tweets[0].text;

if __name__ == "__main__":
    app.run()
