import os
import json
import time
import transpositionCipher
from pathlib import Path


class AccessGetter:
    targetFile = None
    jsonDataDict = None
    jsonFilename = ".projectData.json"

    # key = 'mDn5S2JoGGMVw5CkfmBtNRV_dYfhLqNByesoPZhJVuQ='
    # TODO: Use this base64 encoded string as key when upgrading encryption program

    def __init__(self, fileKey = None, logger = None, verbose = False):

        """ Note: if verbose = True, data contained in filename WILL be displayed """

        self.logger = logger
        self.verbose = verbose

        if (fileKey):
            self.jsonFilename = fileKey
        self.path = str(Path.home()) + "/.ssh/encrypted-data"
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        return

    def __encryptData(self, text, outputFilename):
        myMode = "encrypt"
        outputFile = open(outputFilename, 'w+')

        if (self.verbose):
            print('%sing...' % (myMode.title()))
        startTime = time.time()
        translated = transpositionCipher.encrypt(text, 7)
        totalTime = round(time.time() - startTime, 2)
        if (self.verbose):
            print('%sion time: %s secondes' % (myMode.title(), totalTime))
        outputFile.write(translated)
        outputFile.close()

    def getDict(self, filename = None):

        """

        :param:
            filename = The file in which the json data is contained. If no filename, uses the name given in Ctor.
        If no filename given in Ctor, throws exception

        If file has extension '.encrypted.json', will be decrypted. If not, an encrypted copy will be made.

        :return:
            Dictionary containing data from .json file

        :example:
        >>>
        accessgetter = AccessGetter("notEncryptedFile.json")
        dict = accessgetter.getDict() # Creates notEncryptedFile.encrypted.json

        dict = accessgetter.getDict(".twitter.encrypted.json")

        Note: AccessGetter.filename is replaced when calling getDict with a filename

        """

        if filename:
            self.jsonFilename = filename
            self.jsonDataDict = None
            filename = filename.lower()
        elif not filename and not self.jsonDataDict and not self.jsonFilename:
            raise RuntimeError("AccessGetter.getDict: failed to provide valid .json file to get Dict from")
        if self.jsonDataDict:
            return self.jsonDataDict
        else:
            return self.__getDictFromJson()

    def __getDictFromJson(self):
        if not os.path.exists(self.path + '/' + self.jsonFilename + ".json") and not\
                os.path.exists(self.path + '/' + self.jsonFilename + ".encrypted.json"):
            raise RuntimeError("AccessGetter.getDict: failed to provide valid .json file to get Dict from")

        if os.path.exists(self.path + '/' + self.jsonFilename + ".json"):
            jsonfile = open(self.path + '/' + self.jsonFilename + ".json")
            self.jsonFilename = self.jsonFilename + ".json"
        else:
            jsonfile = open(self.path + '/' + self.jsonFilename + ".encrypted.json")
            self.jsonFilename = self.jsonFilename + ".encrypted.json"

        if not self.jsonFilename.lower().endswith('.encrypted.json'):
            name = os.path.splitext(self.path + '/' + self.jsonFilename)[0]
            outputFileName = name + '.encrypted.json'
            readString = jsonfile.read()
        else:
            print("Unciphering")
            outputFileName = self.jsonFilename
            readString = transpositionCipher.decrypt(jsonfile.read(), 7)

        if (self.verbose):
            print("File " + self.jsonFilename + " contains: \n" + readString)
        jsonfile.close()
        self.jsonDataDict = json.loads(readString)

        self.__encryptData(readString, outputFileName)
        return self.jsonDataDict

ag = AccessGetter(None, None, True)
dict = ag.getDict("twitter")

# TODO: Code a better encryption/decryption system
# TODO: Write doc/comments
# TODO: Unit testing via template https://github.com/hayj/SystemTools/blob/master/systemtools/test/basics.py
