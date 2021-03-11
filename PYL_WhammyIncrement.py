import os
import boto3


def lambda_handler(event, context):
    
    '''initialize table object'''
    dynamodb = boto3.resource('dynamodb')
    pylstats = dynamodb.Table('PYL_Stats')

    '''capture UUID'''
    sessionID = event.get('Details').get('ContactData').get('ContactId')
    #sessionID= '1234'


    '''Get Item from Database'''
    response = pylstats.get_item(
        TableName = 'PYL_Stats',
        Key = {
            'CallSessionUID' : sessionID
        }
    )
    item = response['Item']
    
    '''get'''
    currentWhammy = item.get('CurrentWhammy')
    currentWhammy += 1
    
    currentScore = item.get('CurrentScore')
    newcurrentScore = int(currentScore / 2)
    
    '''update new whammy value in DB'''
    pylstats.update_item(
        Key = {
            'CallSessionUID' : sessionID,
        },
        UpdateExpression='SET CurrentWhammy = :val1, CurrentScore = :val2',
        ExpressionAttributeValues={
            ':val1': currentWhammy,
            ':val2': newcurrentScore
        }
    )
    
    
    success = {}
    
    '''whammy gameover check'''
    if currentWhammy >= 4:
        success['gameover'] = 'True'
    
    
    
    ''''required return'''
    success['run'] = 'True'
    return success  
    
    





