import random
import pickle
import requests

fileOpen = open('namesPickle.pickle','rb')
likesNames = pickle.load(fileOpen)
fileOpen.close()

fileOpen = open('idPickle.pickle','rb')
likesId = pickle.load(fileOpen)
fileOpen.close()

luckyNumber = int(round(random.uniform(0, 99)))

luckyId = likesId[luckyNumber]
luckyName = likesNames[luckyNumber]

token = 'EAACEdEose0cBABvUNPYLtsE2i2eZBrVZAomAE0CCWOgcwyZAR5f7aqjr4tVZCSiGyjMrxZBNBBpkCSZBgZAjfMfqqVrGbbj7bBNMlwgbK5ZAqP91bMkVfbWIywOXvoT3NsIsDpOWoiX4bUOoxWgK62RwFDN9dyB9nh7Dnm1CKQCZAeuLw5ILxK40KZCrpG0FRF2AEZD'

url = "https://graph.facebook.com/v2.11/"+luckyId+"?fields=feed%7Bmessage%2Cfull_picture%7D&access_token="+token


postJSON = requests.get(url).json()

luckyMessageNumber = int(round(random.uniform(0, len(postJSON['feed']['data'])-1)))

print luckyName

if postJSON['feed']['data'][luckyMessageNumber].has_key('message'):
    print postJSON['feed']['data'][luckyMessageNumber]['message']

if postJSON['feed']['data'][luckyMessageNumber].has_key('full_picture'):
    print "Image URL "+postJSON['feed']['data'][luckyMessageNumber]['full_picture']

