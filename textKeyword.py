import httplib, urllib, json, pickle

accessKey = '92c6e0a9e5154377858cc7860eda4c32'

f = open('backupData.pickle', 'rb')

listToReturn = pickle.load(f)

f.close()

uri = 'westcentralus.api.cognitive.microsoft.com'
path = '/text/analytics/v2.0/keyPhrases'

def GetKeyPhrases (documents):
    "Gets the sentiments for a set of documents and returns the information."

    headers = {'Ocp-Apim-Subscription-Key': accessKey}
    conn = httplib.HTTPSConnection (uri)
    body = json.dumps (documents)
    conn.request ("POST", path, body, headers)
    response = conn.getresponse ()
    return response.read ()

NetContent = []
for i in range(len(listToReturn)):
    NetContent.append({'id':str(i), 'language': 'en', 'text': listToReturn[i]['content']})
'''
documents = { 'documents': [
    { 'id': '1', 'language': 'en', 'text': 'Runs now starting to come a little easier for SA as Amla (42) and Elgar (38) take their partnership to 88, the highest of the match. This after the first wicketless session of the Test this morning. The target is also now below 150. SA 93/1 #ProteaFire #SAvIND' }
]}
'''
documents = { 'documents': NetContent}

result = json.loads(GetKeyPhrases (documents))
#print (json.dumps(json.loads(result), indent=4))

doc = result['documents']
for i in range(len(doc)):
    cTags = ""
    ida = int(doc[i]['id'])
    for j in range(min(3, len(doc[i]['keyPhrases']))):
        cTags = cTags + " " + doc[i]['keyPhrases'][j]
    listToReturn[ida]["contentTags"] = cTags

f = open('backupData.pickle', 'wb')
pickle.dump(listToReturn, f)
f.close()
