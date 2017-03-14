# Social-Network-Explorer

Yan Jiang, Chuyang Wang

<strong>To run this app locally, download the code. Go to the directory of the downloaded folder, run “pip install -r requirements.txt” and then run “python spotify.py” with python 3.5.2.</strong>


Tweets About Your Favorite Artists In Music

We used Spotify Web API and Twitter API in this assignment. We only need user’s authorization on Spotify. But we do need the user to be an active Spotify user with  listening history longer than 6 months.

The application we built will get user's most listened 25 artists on Spotify, and 5 related artists of the 25 artists. Then, when user click the picture of their top artists or the name of the related artist, the app will show 20 tweets about that artist. The crawled data is a mixed collection of most popular and most recent tweets related to this certain artist. 

We used the Personalization Endpoint of Spotify Spotify Web API to get a user's top artists, which is based their listening history. The we used Artist’s Related Artists Endpoint of Spotify Web API to get the artists' related artists, who the user might also be interested in. We also used the User Profile Endpoint of Spotify to show user’s account information in our app. 
Tweets related to a certain artist is obtained by utilizing the search GET search/tweets endpoint of Twitter, using the Tweepy library. 

We used Python and Flask to build this web app, and we deployed the app onto heroku. 
To run this app locally, download our code from https://github.com/Yan-J/Social-Network-Explorer. Go to the directory of the folder, run “pip install -r requirements.txt” and then run “python spotify.py” with python 3.5.2.

Spotify OAuth Code is from: https://github.com/ecliu110/Spotify-OAuth-2.0-Python

