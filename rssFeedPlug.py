import feedparser
import time


class Packet:
    title = ''
    text = ''
    date = None
    time = None
    language = ''
    email = ''
    url = ''
    imageUrl = ''

    def __init__(self, title='', text='', url='', imageUrl='', date=None, time=None, language='', email=''):
        self.title = title
        self.text = text
        self.url = url
        self.imageUrl = imageUrl
        self.date = date
        self.time = time
        self.language = language
        self.email = email

    @staticmethod
    def buildPacket(title='', text='', url='', imageUrl='', date=None, time=None, language='', email=''):
        return Packet(title, text, url, imageUrl, date, time, language, email)


class RssFeedPlug:
    waitTimer = 60
    source = None

    def __init__(self, source, timer=60):
        if timer >= 5:
            self.waitTimer = timer
        if source:
            self.source = source
        else:
            raise RuntimeError("No source provided for RSS feed")

    def getConstantFeed(self):
        while 1:
            data = feedparser.parse(self.source)
            time.sleep(self.waitTimer)
            print(data)

    @staticmethod
    def getPunctualFeed(rss):
        return feedparser.parse(rss)


# TODO: Functions to build a list of Packets from each RSS feed (in callback from async call ?)

print(RssFeedPlug.getPunctualFeed("http://9gag-rss.com/api/rss/get?code=9GAGFresh&format=2"))
rfp = RssFeedPlug("http://9gag-rss.com/api/rss/get?code=9GAGFresh&format=2", 10)
rfp.getConstantFeed()
exit(0)