import tweepy


class LRITwitterListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        if status_code == 420:
            exit(2)

    def on_connect(self):
        print("Connected !")

    def on_data(self, raw_data):
        print(raw_data)


mystreamListener = LRITwitterListener()

auth = tweepy.OAuthHandler("dq9tBwtaU0EviD0mKTle4cNgk", "wrKMFtyjNpKHmfbbeMVa3T5NsQHFsmSdX2VyP0CdyNhbB0nr84")
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token')


auth.set_access_token("937684721164869632-GOOZrgIe5RfKISuh1tMBVg1RJDkgFap", "CBSEnDhrrD7TE1uAqxUTUUcXdwACuXwRU4YhAIVA5bGTu")


api = tweepy.API(auth)

mystream = tweepy.Stream(auth=api.auth, listener=mystreamListener)
mystream.timeout = 60
mystream.userstream(encoding='utf-8')


exit(0)
