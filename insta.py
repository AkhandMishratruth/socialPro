from InstagramAPI import InstagramAPI
import pickle, time
from analyze import *

api=InstagramAPI("computer_4517","computer_network")
if (api.login()):
    api.getSelfUserFeed()
    print(api.LastJson)
    print("LoginSuccess")

else :
    print("Can't Login")

Name = ''
profilePic = ''
content = ''
imageURL = ''
timestamp = ''

api.getProfileData()
result=api.LastJson
#print(result)
api.timelineFeed()

feed=api.LastJson

dataToReturn = []

def instaFeed():
    for i in range(feed['num_results']):
        try:
            imageURL = feed['items'][i]['image_versions2']['candidates'][0]['url']
            timestamp = feed['items'][i]['device_timestamp']
            Name = feed['items'][i]['user']['username']
            profilePic = feed['items'][i]['user']['profile_pic_url']
            content = feed['items'][i]['caption']['text']
            imageAnalysis = simplifyImageJson(str(imageURL))
            time.sleep(3)
            tempDic = {"from":"Instagram","Name":Name, "adult":imageAnalysis["adult"], "textInImage":imageAnalysis["textInImage"] , "caption": imageAnalysis["caption"], "accentColor": imageAnalysis['accentColor'], "profilePic":profilePic, "content":content, "contentTags":"", "imageURL":imageURL, "timestamp":timestamp}
            dataToReturn.append(tempDic)
            print "inner "+str(i)
        except KeyError:
            continue

for i in range(13):
    print "outer "+str(i)
    instaFeed()

f = open('instaFeed.pickle','wb')
pickle.dump(dataToReturn, f)
f.close()
