'''function displays live players by being triggered by PYL_stats DDB table, dumps changed valeus to new 
DDB table (PYL_LiveGame). Deletes PYL_LiveGame entries after 4 Whammy's'''

import boto3
import json
import random

def lambda_handler(event, context):
    #print (event)
    
    '''Grab records from new DDB request'''
    action = event.get("Records")[0].get("eventName")
    callerID = event.get("Records")[0].get("dynamodb").get("NewImage").get("CallerID").get("S")
    currentScore = int(event.get("Records")[0].get("dynamodb").get("NewImage").get("CurrentScore").get("N"))
    currentWhammy = int(event.get("Records")[0].get("dynamodb").get("NewImage").get("CurrentWhammy").get("N"))
    currentSpinCount = int(event.get("Records")[0].get("dynamodb").get("NewImage").get("CurrentSpinCount").get("N"))
    print ("Caller ID:  {}, Score: {}, Spin Count: {}, Whammy Count: {}".format(callerID, currentScore, currentSpinCount, currentWhammy))
    
    '''hide some of the caller ID settings'''
    callerIDlist = list(callerID)
    callerIDlist.remove("+")
    callerIDlist.remove("1")
    callerIDlist.insert(3,"-")
    callerIDlist.insert(7,"-")
    
    callerIDlist.insert(0,"x")
    callerIDlist.insert(0,"x")
    callerIDlist.insert(0,"x")
    callerIDlist.pop(3)
    callerIDlist.pop(3)
    callerIDlist.pop(3)  
    
    callerIDlist.insert(4,"x")
    callerIDlist.insert(4,"x")
    callerIDlist.insert(4,"x")
    callerIDlist.pop(7)
    callerIDlist.pop(7)
    callerIDlist.pop(7)    
    joinedList = "".join(callerIDlist)
    print(joinedList)
    
    
    
    # if currentWhammy < 4:
    writeToDB(joinedList, currentScore, currentWhammy, currentSpinCount)
    # else:
    #     deleteFromDB(callerID)
    return event
    
    
def writeToDB(a,b,c,d):
    '''initialize table object'''
    dynamodb = boto3.resource('dynamodb')
    pylLive = dynamodb.Table('PYL_LiveGame')

    '''store values on initialization table'''
    pylLive.put_item(
        Item = {
            'CallerID' : a,
            'CurrentScore' : b,
            'CurrentSpinCount': d,
            'CurrentWhammy' : c,
            'ListKey-index' : random.randint(0,1000)
        }
    )
    
def deleteFromDB(a):
    dynamodb = boto3.resource('dynamodb')
    pylLive = dynamodb.Table('PYL_LiveGame')
    
    pylLive.delete_item(
    Key={
        'CallerID': a
    }
)