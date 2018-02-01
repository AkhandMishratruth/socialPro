import httplib, urllib, base64, json

def imageMSapi(link, service):
    subscription_key = '1af635b4b9684674bb4743026f5aa229'
    
    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    headers = {
        # Request headers.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.urlencode({
        # Request parameters. All of them are optional.
        'visualFeatures': 'Categories,Description,Color,Adult',
        'language': 'en',
    })
    
    # The URL of a JPEG image to analyze.
    body = str({'url': link})

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/" + service + "?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
##        print ("Response:")
##        print json.loads(json.dumps(parsed, sort_keys=True))
        return json.loads(json.dumps(parsed, sort_keys=True))
        conn.close()

    except Exception as e:
        print('Error:')
        print(e)

def simplifyImageJson(link):
    accentColor = ""
    caption = ""
    textInImage = ""
    adult = ""
    
##    print ">>>>>> "+link
    data = imageMSapi(link, "analyze")
    
    if data.has_key('color'):
        if data['color'].has_key('accentColor'):
            accentColor = data['color']['accentColor']

    if data.has_key('description'):
        if data['description'].has_key('captions'):
            if len(data['description']['captions'])>0:
                if data['description']['captions'][0].has_key('text') and data['description']['captions'][0]['confidence'] > 0.3:
                    caption = data['description']['captions'][0]['text']

    if data.has_key('adult'):
        adult = data['adult']['isAdultContent']
        
    data = imageMSapi(link, "ocr")
    if data.has_key('regions'):
        if len(data['regions'])>0:
            numberOfLines = len(data['regions'][0]['lines'])
            for i in range(numberOfLines):
                numberOfWords = len(data['regions'][0]['lines'][i]['words'])
                for j in range(numberOfWords):
                    textInImage = textInImage + " " + data['regions'][0]['lines'][i]['words'][j]['text']
##    print str({"accentColor":accentColor,"caption":caption,"textInImage":textInImage})                      
    return {"accentColor":accentColor, "adult":adult,"caption":caption,"textInImage":textInImage}
