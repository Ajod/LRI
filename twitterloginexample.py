import accessGetter
import mystreamlistener

"""
    Instantiate an AccessGetter searching for 
    ~/.ssh/encrypted-data/twitter.json or twitter.encrypted.json
    
    Get a dictionary of login data from json file
    
    Set the data in an instance of TwitterListener
    
    Connect to the Twitter API and start listening.
"""

accessGetter = accessGetter.AccessGetter("twitter")

logindata = accessGetter.getDict()

twstream = mystreamlistener.LRITwitterListener()

twstream.setLoginData(logindata["consumerid"],
                      logindata["consumersecret"],
                      logindata["accesstoken"],
                      logindata["accesstokensecret"])
twstream.connectAPI()
twstream.startListening()

exit(0)