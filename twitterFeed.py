from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pickle, json
from analyze import *

cKey = 'XvjOdD07JCr4UbQMASplOojg3'
cSecret= 'RhRpmKFRp6DXgVapFeZ3I1vVMdbFwf0JdKMj1VfYAnFAr4PkiK'
atoken = '843014506334707712-EHxe6eW3wS2NmwtnvxkCaQwSgTf2hJC'
asecret = '3RLDTihyKsrM8RaNmCEERrbtlVGz8JHE2BDcSv3gKisr0'

twData = []
def twitterData(data):
    print type(data)
    content = ""
    imageURL = ""
    timestamp = data['created_at']
    profilePicUrl = data['user']['profile_image_url']
    contentTags = ""
    imageAnalysis = ""
    Name = data['user']['name']    

    if data.has_key('extended_tweet'):
        content = data['extended_tweet']['full_text']
        if data['extended_tweet']['entities'].has_key("media_url_https"):
            imageURL = str(data['extended_tweet']['extended_entities']["media_url_https"])
            imageAnalysis = simplifyImageJson(imageURL)

            adult = imageAnalysis["adult"]
            textInImage = imageAnalysis["textInImage"]
            caption = imageAnalysis["caption"]
            accentColor = imageAnalysis['accentColor']
        
    return {"Name":Name, "adult":adult, "textInImage":textInImage , "caption": caption, "accentColor": accentColor, "profilePic":profilePicUrl, "content":content, "contentTags":contentTags, "imageURL":imageURL, "timestamp":timestamp}

class listener(StreamListener):
    def on_data(self, data):
        print data
        twData.append(json.loads(str(data)))
        return True

    def on_error(self, status):
        print status

auth = OAuthHandler(cKey, cSecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=['cars', 'bikes', 'AI', 'Microsoft', 'Google', 'smartphone', 'Windows', 'laptop', 'programming', 'android'])
##f = open('twitter.pickle', 'wb')
##f.close()
