from flask import Flask, abort, request, render_template
from uuid import uuid4
import requests
import requests.auth
import urllib
import string
import random

SPOTIFY_APP_ID = 'b9d97275936943d6965ffbdd5e402238'
SPOTIFY_REDIRECT_URI = 'http://localhost:5000/callback'
SPOTIFY_CLIENT_SECRET = '8ac92255fb684073b02f61e38f96cc34'
RANDOM_STATE = ''

app = Flask(__name__)

#----------------------Get info from Twitter through Tweepy----------------------#
import tweepy

#Create variables for each key, secret, token.
consumer_key = 'hrABYWoeNcdDgyMYUPqlcITNi'
consumer_secret = '8KkiJEgeJySQ8ZFDA2ywHPx2cagifHqiXS7jxcsCWDtLPGV59K'
access_token = '838796084038230016-L8xC5JUjkDxUvfNJR4iZACE5QIKlXMG'
access_token_secret = 'jhQC3kWgc8SbkmlMnJ5965UDddeV61EbGbqcUnfzI3DuQ'

#Set up OAuth and integrate with API.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Prompt login
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with spotify</a>'
    return render_template("index.html", requestURL=make_authorization_url())

# Create authorzation url
def make_authorization_url():
    global RANDOM_STATE
    RANDOM_STATE = generateRandomString(16)
    params = {"client_id": SPOTIFY_APP_ID,
              "response_type": "code",
              "redirect_uri": SPOTIFY_REDIRECT_URI,
              "state": RANDOM_STATE,
              "scope": "user-top-read"
              }
    url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    return url

# Callback page
@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state', '')
    # Check state, get access token if valid
    if state == RANDOM_STATE:
        artists = []
        token_json = get_token(code)
        user_info = get_userInfo(token_json['access_token'])
        artist_infoa = get_topArtist(token_json['access_token'])
        artist_info = artist_infoa['items']
        url_list = []
        image_list = []
        for item in artist_info:
            print (item['name'])
            image_list.append(item['images'][1]['url'])
            url_list.append(urllib.parse.quote_plus(item['name']))

        profile_img = user_info['images']
        return render_template("profile.html",image_list=image_list,user_json=user_info, profile_img=profile_img, artist_json=artist_info, atrist_url=url_list)
    # invalid state, abort
    else:
        abort(403)
        
@app.route("/twts/")
@app.route("/twts/<name>/")
def twts(name = None):
    twt_list = get_tweets(name)
    return render_template('twt.html', twt_list=twt_list)

# Use code to obtain access token, refresh token
def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(SPOTIFY_APP_ID, SPOTIFY_CLIENT_SECRET)
    headers = {'Authorization': 'Basic '}
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": SPOTIFY_REDIRECT_URI}
    response = requests.post("https://accounts.spotify.com/api/token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()
    return token_json

# Use access token to get user info
def get_userInfo(access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    me_json = response.json()
    return me_json

def get_topArtist(access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get("https://api.spotify.com/v1/me/top/artists?limit=50&offset=0", headers=headers)
    artist_json = response.json()
    return artist_json

def generateRandomString(len):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len))

def get_tweets(keyword):
    twt_list = []
    twt_list = api.search(q = keyword, count = 20)
    return twt_list

if __name__ == "__main__":
    app.run(debug=True)
