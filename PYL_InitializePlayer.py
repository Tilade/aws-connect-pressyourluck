'''Function initilized a user into the PYL Loop
Stored values that are referenced in later functions'''



import boto3
import os
import datetime

def lambda_handler(event, context):

    '''initialize table object'''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')

    '''capture UUID and CID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    callerID = event.get('Details').get('ContactData').get('CustomerEndpoint').get('Address')
    date = str(datetime.datetime.today())
    '''store values on initialization table'''
    pylstats.put_item(
        Item = {
            'CallSessionUID' : sessionID,
            'CallerID' : callerID,
            'CurrentScore' : 0,
            'CurrentSpinCount': 0,
            'CurrentWhammy' : 0,
            'DateTime' : date,
            'ListKey' : 1
            
        }
    )
    
    ''''required return'''
    success = {'run' : 'True'}
    
    print (date)
    return success
    
