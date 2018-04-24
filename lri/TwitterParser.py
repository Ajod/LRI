import parser
import json
from unshortener.unshortener import *
from domainduplicate import config as dpConfig
dpConfig.useMongodb = False

class TwitterParser(parser.Parser):
    def __init__(self):
        super().__init__(section="TWITTER")

    # TODO: Parse tweets
    # Returns a dict from read text containing keys in keywordlist
    def parse(self, text):
        pass

    # Returns a dict from a file, either filepath or fileobject must be valid or an exception will be raised
    def process(self, filepath=None, fileobject=None):
        for line in open(filepath, 'r'):
            yield json.loads(line)


t = TwitterParser()
klist = t.getKeywordList()
val = t.process("tweets.json")
data = []
for i in val:
    data.append(i)

for field in data[1]['entities']:
    print (field)
print(data[1]['entities']['urls'])
print(data[1]['entities']['urls'][0]['expanded_url']) # Scrap urls from this

uns = Unshortener\
    (shortenersDomainsFilePath=homeDir() + "/LRI/data/shorteners.txt", # Set the file path
        useProxy=False,
        randomProxyFunct=None,
        proxy=None,
        serializableDictParams=\
        {
            "limit": 10000000,
            "useMongodb": False,
            "name": "unshortenedurls",
            "cacheCheckRatio": 0.0,
            "mongoIndex": "url",
        }
)

final = uns.unshort(data[1]['entities']['urls'][0]['expanded_url'])
uns.data.save()
print(final)