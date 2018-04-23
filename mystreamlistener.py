import tweepy
import os
import sys


class LRITwitterListener(tweepy.StreamListener):

    consumerSecret = None
    consumerKey = None
    accessToken = None
    accessTokenSecret = None
    api = None
    auth = None
    output = None
    tweetmaxnumber = 0
    currenttweets = 0

    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            exit(2)

    def on_connect(self):
        print("Connected !")

    def on_data(self, raw_data):
        if self.tweetmaxnumber > 0:
            if self.currenttweets >= self.tweetmaxnumber:
                raise RuntimeWarning("Specified number of tweets achieved")
        if self.output is None:
            print(raw_data)
        else:
            self.output.write(raw_data)
        self.currenttweets += 1

    def setOutput(self, fd):
        self.output = fd

    def setMaxTweets(self, max):
        self.tweetmaxnumber = max

    def setLoginData(self, consumerkey, consumersecret, accesstoken=None, accesstokensecret=None):
        self.consumerKey = consumerkey
        self.consumerSecret = consumersecret
        self.accessToken = accesstoken
        self.accessTokenSecret = accesstokensecret
        self.auth = tweepy.OAuthHandler(self.consumerKey, self.consumerSecret)

    def connectAPI(self):
        if not self.consumerKey or not self.consumerSecret or not self.accessToken or not self.accessTokenSecret:
            raise RuntimeError("A required authentication token wasn't set by the user")
        self.auth.set_access_token(self.accessToken, self.accessTokenSecret)
        self.api = tweepy.API(self.auth)

    def startListening(self):
        mystream = tweepy.Stream(self.api.auth, listener=self)
        mystream.timeout = 60
        mystream.userstream(encoding='utf-8')
