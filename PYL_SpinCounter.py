import boto3
import os


def lambda_handler(event, context):
	
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    #sessionID = "1234"
    ''''database connection '''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')
    response = pylstats.get_item(
    TableName = 'PYL_Stats',
    Key = {
        'CallSessionUID' : sessionID
        }
    )
    item = response['Item'] 
    currentSpin = item.get('CurrentSpinCount')
    currentSpin += 1
    pylstats.update_item(
        Key = {
            'CallSessionUID' : sessionID,
        },
        UpdateExpression='SET CurrentSpinCount = :val1',
        ExpressionAttributeValues={
            ':val1': currentSpin
        }
    )
    run = {}
    run['executed'] = 'Success'
    
    
    '''whammy gameover check'''
    currentWhammy = item.get('CurrentWhammy')
    if currentWhammy >= 4:
        run['gameover'] = 'True'
    
    return run 
    