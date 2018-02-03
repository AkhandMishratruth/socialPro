import random
import pickle
import requests
import json
from flask import jsonify
import datetime
import rake
import httplib, urllib, base64, json
from analyze import *
from random import shuffle
import time

def fbSinglePost():
    toRet = []
##    fileOpen = open('namesPickle.pickle','rb')
##    likesNames = pickle.load(fileOpen)
##    fileOpen.close()

    fileOpen = open('fbLikes.pickle','rb')
    likesId = pickle.load(fileOpen)
    fileOpen.close()

    #luckyNumber = int(round(random.uniform(0, 99)))

    #luckyId = likesId[luckyNumber]
    #luckyName = likesNames[luckyNumber]

    token = 'EAACEdEose0cBAEFvIvSqZBR3vwGqaSuD98pyQy2dDZAeQ8PYwdb3OWlMmZBUqLs60iEWaiJH1ZCgEUve5I0Cn4toGqhVLscZBYm64LTsjCelxtDdVGyr3dk7OzeZCbDhtzPgQEGxTD97ZBxQfmYxU3xG5xm5sMAWGj6fuy2pG2EXl06K4gdVBTIz2UIh98vorwZD'

    for i in range(len(likesId)):
        print "outer "+str(i)

        url = "https://graph.facebook.com/v2.11/"+likesId[i]+"?fields=id%2Cfeed%7Bfull_picture%2Cmessage%2Ccreated_time%7D%2Cname%2Cpicture&access_token="+token

        postJSON = requests.get(url).json()

        if not postJSON.has_key("feed"):
            return None

        for j in range(min(3, len(postJSON['feed']['data']))):
            print "inner "+str(j)
                    
            content =""
            imageURL = ""
            timestamp = ""
            profilePicUrl = ""
            contentTags = ""
            pictureType = "full_picture"
            imageAnalysis = ""
            
            if postJSON['feed']['data'][j].has_key('message'):
                content = postJSON['feed']['data'][j]['message']
                '''
                contentTagsList = keywordProvider(content)
                for i in range(min(3, len(contentTagsList))):
                    if(len(contentTags)<40):
                        contentTags = contentTags + " " + contentTagsList[i][0]
                contentTags = contentTags.strip()
                tagArray = contentTags.split(" ")
                contentTags = ""
                for i in range(len(tagArray)):
                    if(len(contentTags)<35):
                        contentTags = contentTags + " " + tagArray[i]
                contentTags = contentTags.strip()
                '''    
            if postJSON['feed']['data'][j].has_key(pictureType):
                imageURL = postJSON['feed']['data'][j][pictureType]
##        imageAnalysis = str(simplifyJson(imageURL))
##        print imageAnalysis

            if postJSON['feed']['data'][j].has_key("created_time"):
                t = timeToString(postJSON['feed']['data'][j]["created_time"])

            if postJSON['picture']['data'].has_key("url"):
                profilePicUrl = postJSON['picture']['data']['url']
                
                imageAnalysis = simplifyImageJson(str(imageURL))
                
            onePostdict = {'from':"Facebook","Name":postJSON['name'],"adult":imageAnalysis["adult"],"textInImage":imageAnalysis["textInImage"] , "caption": imageAnalysis["caption"], "accentColor": imageAnalysis['accentColor'], "profilePic":profilePicUrl, "content":content, "contentTags":contentTags, "imageURL":imageURL, "timestamp":t}
            toRet.append(onePostdict)
            time.sleep(3)
    
    f = open('fbData.pickle','wb')
    pickle.dump(toRet, f)
    f.close()

def timeToString(t):
    t = t.split("+")[0].split("T")[0]+" "+t.split("+")[0].split("T")[1]
    datetime_obj = datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    datetime_obj = datetime_obj + datetime.timedelta(hours=5.5)
    timestampstring = str(datetime_obj)
    date = timestampstring.split(" ")[0]
    time = timestampstring.split(" ")[1]
    date = date.split("-")[2]+"-"+date.split("-")[1]+"-"+date.split("-")[0]
    return time+" "+date

def keywordProvider(text):
    stoppath = "SmartStoplist.txt"
    rake_object = rake.Rake(stoppath)
    return rake_object.run(text)

def posts(index):
    listToReturn = []
    f = open('instaFeed.pickle','r')
    listMain = pickle.load(f)
    f.close()
##    f = open('twitterData.pickle','r')
##    twi = pickle.load(f)
##    f.close()
##    for i in range(20):
##        listMain.append(twi[i])
##    shuffle(listMain)
    for i in range(index, index + 10):
        listToReturn.append(listMain[i])
    shuffle(listMain)
    return json.dumps({"listArray":listToReturn})
