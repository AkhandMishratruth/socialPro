import pickle
from analyze import *

f = open('twitter.pickle','r')
data = pickle.load(f)
f.close()

def twitterData(data):
    print type(data)
    content = ""
    imageURL = ""
    timestamp = ""
    profilePicUrl = ''
    contentTags = ""
    imageAnalysis = ""
    Name = ""
    adult = ''
    textInImage = ''
    caption = ''
    accentColor = ''

    
    if data.has_key('user'):
        Name = data['user']['name']
        profilePicUrl = data['user']['profile_image_url']

    if data.has_key('created_at'):
        timestamp = data['created_at']
    if data.has_key('text'):
        content = data['text']
    if data.has_key('extended_tweet'):
        if data['extended_tweet']['entities'].has_key("media"):
            imageURL = str(data['extended_tweet']['entities']['media'][0]["media_url_https"])
            imageAnalysis = simplifyImageJson(imageURL)

            adult = imageAnalysis["adult"]
            textInImage = imageAnalysis["textInImage"]
            caption = imageAnalysis["caption"]
            accentColor = imageAnalysis['accentColor']
        
    return {"from":"Twitter","Name":Name, "adult":adult, "textInImage":textInImage , "caption": caption, "accentColor": accentColor, "profilePic":profilePicUrl, "content":content, "contentTags":contentTags, "imageURL":imageURL, "timestamp":timestamp}

dataToSave = []
for i in range(100):
    print i
    dataToSave.append(twitterData(data[i]))

f = open('twitterData.pickle', 'wb')
pickle.dump(dataToSave, f)
f.close()
