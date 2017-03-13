from flask import Flask, abort, request, render_template
from uuid import uuid4
import requests
import requests.auth
import urllib
import string
import random

SPOTIFY_APP_ID = 'b9d97275936943d6965ffbdd5e402238'
SPOTIFY_REDIRECT_URI = 'http://snexplorer.herokuapp.com/callback'
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
        profile_img = user_info['images']
        url_list = []
        image_list = []
        related_artist_list=[]
        name_url=[]
        artist_num=len(artist_info)
        for item in artist_info:
            if len(item['images'])>1:
                image_list.append(item['images'][1]['url'])
            else:
                image_list.append('https://cdn4.iconfinder.com/data/icons/eldorado-user/40/user-128.png')
            url_list.append(urllib.parse.quote_plus(item['name']))
            related_artist_list.append(get_related_artist(item['id']))
            print(item['name'])
            print(get_related_artist(item['id']))
        for item in related_artist_list:
            for name in item:
                name_url.append(urllib.parse.quote_plus(name))
        return render_template("profile.html",artist_num=artist_num,name_url=name_url,related_artist_list=related_artist_list,image_list=image_list,user_json=user_info, profile_img=profile_img, artist_json=artist_info, atrist_url=url_list)
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

def get_related_artist(artist_id):
    response = requests.get("https://api.spotify.com/v1/artists/"+ artist_id + "/related-artists")
    related_artists = response.json()['artists']
    related_artists_names=[]
    for artist in related_artists:
        related_artists_names.append(artist['name'])
    return related_artists_names[0:5]

def generateRandomString(len):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len))

def get_tweets(keyword):
    twt_list = []
    twt_list = api.search(q = keyword, count = 20, result_type = "mixed")
    return twt_list

if __name__ == "__main__":
    app.run(debug=True)
