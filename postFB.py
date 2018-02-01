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

def fbSinglePost():
    fileOpen = open('namesPickle.pickle','rb')
    likesNames = pickle.load(fileOpen)
    fileOpen.close()

    fileOpen = open('idPickle.pickle','rb')
    likesId = pickle.load(fileOpen)
    fileOpen.close()

    luckyNumber = int(round(random.uniform(0, 99)))

    luckyId = likesId[luckyNumber]
    luckyName = likesNames[luckyNumber]

    token = 'EAACEdEose0cBAKZB1ihZCsCp1ikxRjyZAMAaFkWUl4y9qNHOuqwzm9fc0yr6ZAoDa9BR6NWKx9r1Ufev9mbHFsRCwn5Fd8ssXFYF3NtlUpXhGZC3RX0frERvPiRnXtFd6tpaH08NFW9z4JEh4EZB5m31e87GlcwOmnidUY2y1ivmprF0nBaTZBZCU157b4x49N0ZD'

    url = "https://graph.facebook.com/v2.11/"+luckyId+"?fields=picture%7Burl%7D%2Cfeed%7Bmessage%2Cfull_picture%2Ccreated_time%7D&access_token="+token

    postJSON = requests.get(url).json()
    
    if postJSON.has_key("feed"):
        luckyMessageNumber = int(round(random.uniform(0, len(postJSON['feed']['data'])-1)))
    else:
        return None
    print luckyName

    content =""
    imageURL = ""
    timestamp = ""
    profilePicUrl = ""
    contentTags = ""
    pictureType = "full_picture"
    imageAnalysis = ""

    
    if postJSON['feed']['data'][luckyMessageNumber].has_key('message'):
        content = postJSON['feed']['data'][luckyMessageNumber]['message']
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
        

    if postJSON['feed']['data'][luckyMessageNumber].has_key(pictureType):
        imageURL = postJSON['feed']['data'][luckyMessageNumber][pictureType]
##        imageAnalysis = str(simplifyJson(imageURL))
##        print imageAnalysis

    if postJSON['feed']['data'][luckyMessageNumber].has_key("created_time"):
        t = timeToString(postJSON['feed']['data'][luckyMessageNumber]["created_time"])

    if postJSON['picture']['data'].has_key("url"):
        profilePicUrl = postJSON['picture']['data']['url']
        
    imageAnalysis = simplifyImageJson(str(imageURL))
    
    return {'from':"Facebook","Name":luckyName,"adult":imageAnalysis["adult"],"textInImage":imageAnalysis["textInImage"] , "caption": imageAnalysis["caption"], "accentColor": imageAnalysis['accentColor'], "profilePic":profilePicUrl, "content":content, "contentTags":contentTags, "imageURL":imageURL, "timestamp":t}

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
    f = open('backupData.pickle','r')
    listMain = pickle.load(f)
    f.close()
    f = open('twitterData.pickle','r')
    twi = pickle.load(f)
    f.close()
    for i in range(20):
        listMain.append(twi[i])
    shuffle(listMain)
    for i in range(index, index + 10):
        listToReturn.append(listMain[i])
    return json.dumps({"listArray":listToReturn})
