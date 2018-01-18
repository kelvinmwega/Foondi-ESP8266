
# Purpose of this application:
#      To train Bootcamp students
# prepared for
#      Foondi Workshop
# Author:
#      kelvin mwega <kelvinmk@ke.ibm.com>


import requests
import json
import sys
import os
import urllib2, base64
import datetime

cloudantHost = "https://8d7e1f8e-1f7d-4d64-8788-490379bcbad5-bluemix.cloudant.com/"
cloudantusername = "8d7e1f8e-1f7d-4d64-8788-490379bcbad5-bluemix"
cloudantPassword = "b69d78f8c5aad962b42e278c73cce8238522bdd4a73aaeec73fa8efc11524db3"
levelmeterDB = "levelmeters/_find"

selector = {}
timestamp = {}
reqObj = {}
sortObj = {}
sortArray = []
sort = {}

if __name__ == '__main__':

    try:

        timeRange = raw_input('Fetch data for the past ...hrs ? : ')
        dataLimit = raw_input('Enter the limit of the documents to fetch ? : ')

        print "Fetching %s latest documents for the past %s hours" % (dataLimit, timeRange)

        #get system time in UTC
        currentTime = datetime.datetime.utcnow()
        calcTime = currentTime - datetime.timedelta(hours=int(timeRange))

        #Encode Authorization string using password and username
        base64string = base64.encodestring('%s:%s' % (cloudantusername, cloudantPassword)).replace('\n', '')

        #create headers json object
        headers = {'content-type' : 'application/json', "Authorization" : "Basic %s" % base64string}
        headersObj = json.dumps(headers)

        #convert time to ISO string and add to request body object
        timestamp["$gt"] = calcTime.strftime('%Y-%m-%dT%H:%M:%S.000Z')
        timestamp["$lt"] = currentTime.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        selector["timestamp"] = timestamp
        selector["deviceId"] = "Proto06V"

        sortObj["timestamp"] = "desc"
        sortArray.append(sortObj)

        #Final request body object
        reqObj["selector"] = selector
        reqObj["sort"] = sortArray
        reqObj["limit"] = int(dataLimit)

        print "Request Body Object..."
        print reqObj

        #Post the requst body
        resp = requests.post(data = json.dumps(reqObj), url = cloudantHost+levelmeterDB, headers = headers)

        print "Response status code.. " + str(resp.status_code)

        #check whether request was succesful.
        if (resp.status_code == 200):

            #parse response string into a json object
            respObj = json.loads(resp.text)

            #loop through response array and print the raw height reading from sensor
            #height of this tank is 135cm
            #to calculate real height of the water in tank (135 - doc['payload']['data']['height'])
            print "Collected Data"
            for doc in respObj['docs']:
                #print height in cm and time in utc
                print str(doc['payload'] + doc['timestamp'])

        else:
            print "Encountered error fetching data, check internet connection"



    except Exception as e:
        raise
