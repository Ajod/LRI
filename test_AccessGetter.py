from unittest import TestCase
import accessGetter
from pathlib import Path
import os

print("======================\nStarting unit tests...")


class TestAccessGetter(TestCase):
    def test_initAccessgetter(self):
        self.assertIsNotNone(accessGetter.AccessGetter())
        self.assertIsNotNone(accessGetter.AccessGetter("Test.json"))

    def test_getDict(self):
        handle = open(str(Path.home()) + "/.ssh/encrypted-data/unittest.json", 'w+')
        handle.write("{\
    \"Test1\":\"Value1\",\
    \"Test2\":\"Value2\",\
    \"Test3\":\"AbsolutelyNotValue3\"}")
        handle.close()
        ag = accessGetter.AccessGetter("./unittest.json")
        dict = ag.getDict()
        self.assertIsNotNone(dict)
        self.assertTrue(dict["Test3"] == "AbsolutelyNotValue3")


print("======================\nUnit tests done.")
