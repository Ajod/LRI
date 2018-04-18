import tweepy


class LRITwitterListener(tweepy.StreamListener):

    consumerSecret = None
    consumerID = None
    accessToken = None
    accessTokenSecret = None
    api = None
    auth = None

    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            exit(2)

    def on_connect(self):
        print("Connected !")

    def on_data(self, raw_data):
        print(raw_data)

    def setLoginData(self, consumerid, consumersecret, accesstoken=None, accesstokensecret=None):
        self.consumerID = consumerid
        self.consumerSecret = consumersecret
        self.accessToken = accesstoken
        self.accessTokenSecret = accesstokensecret
        self.auth = tweepy.OAuthHandler(self.consumerID, self.consumerSecret)

    def connectAPI(self):
        if not self.consumerID or not self.consumerSecret or not self.accessToken or not self.accessTokenSecret:
            raise RuntimeError("A required authentication token wasn't set by the user")
        self.auth.set_access_token(self.accessToken, self.accessTokenSecret)
        self.api = tweepy.API(self.auth)

    def startListening(self):
        mystream = tweepy.Stream(self.api.auth, listener=self)
        mystream.timeout = 60
        mystream.userstream(encoding='utf-8')
