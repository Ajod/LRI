from lri.parser import Parser
from systemtools.basics import *
from copy import copy
from ast import literal_eval
import json


class RequiredDataStruct:
    cnt = 0
    args = None
    datadict = None

    def __init__(self, *args):
        self.args = args
        self.datadict = dict.fromkeys(tuple(*args))

    def feedValue(self, key, value):
        self.datadict[key] = value

    def setItem(self, key, value):
        self.datadict[key] = value

    def print(self):
        for key in self.datadict:
            if dictContains(self.datadict, key):
                print(key + ": " + self.datadict[key])

    def __iter__(self):
        return self

    def __next__(self):
        self.cnt += 1
        if self.cnt >= len(self.datadict):
            raise StopIteration
        return self.datadict[self.cnt - 1]

    def __radd__(self, other):
        self.datadict.update(other)
        return self

    def __add__(self, other):
        self.datadict.update(other)
        return self

    def __copy__(self):
        copy = RequiredDataStruct(*self.args)
        copy.datadict.update(self.datadict)
        return copy

    def __lt__(self, other):
        return len(self.datadict) < len(other.datadict)


class RssParser(Parser):

    def __init__(self):
        super().__init__(section="RSS")
        self.parsedDataList = []

    # Returns a list of fully parsed json data from read text containing keys in keywordlist
    def parse(self, filepath=None, fileobject=None, text=None):
        data = []
        if not text and not filepath and not fileobject:
            raise AttributeError("No source provided for parsing")
        if text:
            data.append(json.loads(text))
        elif filepath:
            with open(filepath, 'r') as fd:
                data.append(json.loads(fd.read()))
        else:
            data.append(json.loads(fileobject.read()))
        return data

    # Returns a generator for json-parsed data, either filepath or fileobject must be valid or an exception will be raised
    def process(self, filepath=None, fileobject=None, text = None):
        if not text and not filepath and not fileobject:
            raise AttributeError("No source provided for parsing")
        if text:
            yield(json.loads(text))
        elif filepath:
            with open(filepath, 'r') as fd:
                yield(fd.read())
        else:
            yield(json.loads(fileobject.read()))
        return data

    def parseKeys(self, klist, arr, parsedDataList=None):
        resultstruct = RequiredDataStruct(klist)
        for items in arr:
            if not hasattr(items, '__iter__'):
                continue
            for item in items: # = les catégories du .json
                if hasattr(item, '__iter__'):
                    for key in klist:
                        if key in item:
                            resultstruct.setItem(key, items[key])

                if isinstance(items[item], list):
                    if len(resultstruct.datadict) > 0:
                        self.parsedDataList.append(copy(resultstruct))
                    self.parseKeys(klist, items[item])
        return


t = RssParser()
klist = t.getKeywordList()
data = t.parse(filepath="rssflux.json")
t.parseKeys(klist, data)

links = []
for struct in t.parsedDataList:
    for key in klist:
        if key in struct.datadict and struct.datadict[key] is not None:
            links.append(struct.datadict[key])

links = list(set(links))
links.sort()
for link in links:
    print(link)
