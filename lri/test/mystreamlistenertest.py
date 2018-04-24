from lri import dataencryptor
from lri import mystreamlistener
from unittest import TestCase
from pathlib import Path


class LRITwitterListenerTest(TestCase):

    def testConnection(self):
        de = dataencryptor.DataEncryptor(filename="twitter")
        listener = mystreamlistener.LRITwitterListener()
        auth = de.getDict()
        listener.setLoginData(consumerkey=auth["consumerkey"], consumersecret=auth["consumersecret"],
                              accesstoken=auth["accesstoken"], accesstokensecret=auth["accesstokensecret"])
        try:
            listener.connectAPI()
        except RuntimeError as e:
            print(e.args)
            raise e

    def testGetOneTweet(self):
        de = dataencryptor.DataEncryptor(filename="twitter")
        listener = mystreamlistener.LRITwitterListener()
        auth = de.getDict()
        listener.setLoginData(consumerkey=auth["consumerkey"], consumersecret=auth["consumersecret"],
                              accesstoken=auth["accesstoken"], accesstokensecret=auth["accesstokensecret"])
        try:
            listener.connectAPI()
        except RuntimeError as e:
            print(e.args)
            raise e
        handle = open(str(Path.home()) + "/.ssh/encrypted-data/tweets.json", 'w+')
        listener.setOutput(handle)
        listener.setMaxTweets(1)

        try:
            listener.startListening()
        except RuntimeWarning as e:
            print(e.args)
            handle.seek(0)
        handle.close()
